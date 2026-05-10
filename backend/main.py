import os
import uuid
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# [ZH] 导入配置和各服务模块
# [JA] 設定と各サービスモジュールをインポート
# [EN] Import config and service modules
from backend.config import UPLOAD_DIR
from backend.services.video_service import extract_audio_from_video
from backend.services.stt_service import transcribe_audio
from backend.services.llm_service import analyze_teaching_text

app = FastAPI(title="TeachingAnalyzer API")

# [ZH] 配置 CORS，允许前端跨域请求（React 默认 3000 端口，FastAPI 默认 8000 端口）
# [JA] CORSを設定し、フロントエンドのクロスオリジンリクエストを許可（React:3000, FastAPI:8000）
# [EN] Configure CORS to allow cross-origin requests from the frontend (React:3000, FastAPI:8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # [ZH] 开发环境允许所有来源，生产环境建议指定具体域名 | [JA] 開発環境では全オリジン許可、本番では特定ドメインを推奨 | [EN] Allow all origins in dev; restrict to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/upload_and_analyze")
async def upload_and_analyze(
    file: UploadFile = File(...),
    whisperModel: str = Form("base"),
    ollamaModel: str = Form("qwen2.5:7b"),
    temperature: float = Form(0.3)
):
    """
    [ZH] 接收前端上传的视频，依次执行：保存 -> 提取音频 -> 语音识别 -> 大模型分析
    [JA] フロントエンドからアップロードされた動画を受け取り、保存→音声抽出→音声認識→LLM分析を順に実行
    [EN] Receive uploaded video from frontend and run: save -> extract audio -> transcribe -> LLM analysis
    """
    # [ZH] 1. 校验文件格式，仅接受常见视频格式
    # [JA] 1. ファイル形式を検証し、対応する動画形式のみ受け付ける
    # [EN] 1. Validate file format; only accept common video extensions
    if not file.filename.lower().endswith(('.mp4', '.avi', '.mov')):
        raise HTTPException(status_code=400, detail="只支持视频文件 (.mp4, .avi, .mov)")

    # [ZH] 生成唯一请求 ID 和临时文件路径，避免并发上传时文件互相覆盖
    # [JA] 一意のリクエストIDと一時ファイルパスを生成し、同時アップロード時のファイル上書きを防ぐ
    # [EN] Generate a unique request ID and temp file paths to prevent overwrites under concurrent uploads
    request_id = str(uuid.uuid4())
    video_path = os.path.join(UPLOAD_DIR, f"{request_id}_{file.filename}")
    audio_path = os.path.join(UPLOAD_DIR, f"{request_id}.wav")

    try:
        # [ZH] 2. 将前端传来的文件内容写入本地磁盘
        # [JA] 2. フロントエンドから受け取ったファイル内容をローカルディスクに書き込む
        # [EN] 2. Write the uploaded file content to local disk
        print(f"[{request_id}] 正在保存上传的视频...")
        with open(video_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # [ZH] 3. 从视频中提取音频
        # [JA] 3. 動画から音声を抽出する
        # [EN] 3. Extract audio track from the video file
        print(f"[{request_id}] 正在提取音频...")
        success = await extract_audio_from_video(video_path, audio_path)

        # [ZH] 音频提取失败时立即向前端报错，不继续后续步骤
        # [JA] 音声抽出に失敗した場合、後続処理を行わずフロントエンドにエラーを返す
        # [EN] Abort early and return an error if audio extraction fails
        if not success:
            raise HTTPException(
                status_code=500,
                detail="音频提取失败。请确保视频不是静音的，或尝试更换视频格式（建议使用标准 MP4）。"
            )

        # [ZH] 4. 使用 Whisper 进行语音识别
        # [JA] 4. Whisperを使って音声認識を実行する
        # [EN] 4. Run speech-to-text transcription with Whisper
        print(f"[{request_id}] 正在使用 Whisper ({whisperModel}) 语音识别...")
        stt_result = await transcribe_audio(audio_path, model_name=whisperModel)

        # [ZH] 提取纯文本，供大模型分析使用
        # [JA] LLM分析用にプレーンテキストを取得する
        # [EN] Extract plain text for LLM analysis
        raw_text = stt_result.get("text", "")

        # [ZH] 构造带时间戳的逐字稿字符串（格式：[MM:SS] 文本）
        # [JA] タイムスタンプ付きの文字起こし文字列を生成する（形式：[MM:SS] テキスト）
        # [EN] Build a timestamped transcript string in [MM:SS] text format
        segments = stt_result.get("segments", [])
        formatted_transcription = ""
        for seg in segments:
            start_seconds = int(seg['start'])
            m, s = divmod(start_seconds, 60)
            timestamp = f"[{m:02d}:{s:02d}]"
            formatted_transcription += f"{timestamp} {seg['text'].strip()}\n"

        if not raw_text.strip():
            raise HTTPException(status_code=400, detail="未能从视频中识别出任何有效的语音。")

        # [ZH] 5. 调用大模型对教学行为进行分析
        # [JA] 5. LLMを呼び出して授業行動を分析する
        # [EN] 5. Call the LLM to analyze teaching behavior
        print(f"[{request_id}] 正在调用 Ollama ({ollamaModel}) 进行教学行为分析...")
        analysis_result = await analyze_teaching_text(
            formatted_transcription,
            model_name=ollamaModel,
            temperature=temperature
        )

        # [ZH] 将带时间戳的格式化文本和分析结果一起返回给前端
        # [JA] タイムスタンプ付きのフォーマット済みテキストと分析結果をフロントエンドに返す
        # [EN] Return the formatted timestamped transcript and analysis result to the frontend
        return {
            "status": "success",
            "transcription": formatted_transcription,
            "analysis": analysis_result
        }

    except Exception as e:
        print(f"[{request_id}] 处理过程中发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"内部处理错误: {str(e)}")

    finally:
        # [ZH] 6. 清理临时文件，防止磁盘被大量上传文件撑满
        # [JA] 6. 一時ファイルを削除し、大量アップロードによるディスク不足を防ぐ
        # [EN] 6. Delete temp files to prevent disk exhaustion from repeated uploads
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)


# [ZH] 健康检查接口，用于确认后端服务正常运行
# [JA] ヘルスチェックエンドポイント。バックエンドが正常に稼働しているか確認する
# [EN] Health check endpoint to verify the backend service is running
@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "TeachingAnalyzer Backend is running!"}
