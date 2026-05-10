import os
import asyncio
from moviepy import VideoFileClip


async def extract_audio_from_video(video_path: str, audio_path: str) -> bool:
    """
    [ZH] 在线程池中异步从视频提取音频。成功返回 True，失败返回 False
    [JA] スレッドプールで動画から音声を非同期抽出する。成功時 True、失敗時 False を返す
    [EN] Asynchronously extract audio from a video in a thread pool. Returns True on success, False on failure
    """
    def _extract():
        video = None
        try:
            if not os.path.exists(video_path):
                print(f"错误：找不到视频文件: {video_path}")
                return False

            # [ZH] 加载视频文件
            # [JA] 動画ファイルをロードする
            # [EN] Load the video file
            video = VideoFileClip(video_path)

            # [ZH] 检查音轨是否存在，静音视频无法提取
            # [JA] 音声トラックの存在を確認する。無音動画は抽出不可
            # [EN] Verify the audio track exists; silent videos cannot be extracted
            if video.audio is None:
                print("错误：MoviePy 无法识别该视频的音轨，请检查编码格式。")
                return False

            print(f"正在转换音频: {video_path} -> {audio_path}")

            # [ZH] 强制指定：16000Hz 采样率（Whisper 最佳）、16-bit、单声道、pcm_s16le 编码
            # [JA] 強制指定：16000Hz サンプリング（Whisper 最適）、16bit、モノラル、pcm_s16le コーデック
            # [EN] Force: 16000 Hz sample rate (optimal for Whisper), 16-bit, mono, pcm_s16le codec
            video.audio.write_audiofile(
                audio_path,
                fps=16000,
                nbytes=2,
                codec='pcm_s16le',
                bitrate='128k',
                logger=None  # [ZH] 禁用 MoviePy 进度条输出 | [JA] MoviePy の進捗出力を無効化 | [EN] Suppress MoviePy progress bar output
            )

            # [ZH] 验证输出文件确实存在且不为空
            # [JA] 出力ファイルが存在し、かつ空でないことを確認する
            # [EN] Verify the output file exists and is non-empty
            if os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
                print(f"音频提取成功，文件大小: {os.path.getsize(audio_path)} bytes")
                return True
            else:
                print("错误：音频提取完成但文件不存在或为空。")
                return False

        except Exception as e:
            print(f"提取音频时发生错误: {str(e)}")
            return False
        finally:
            if video:
                # [ZH] 必须关闭，否则临时文件会被系统锁定而无法删除
                # [JA] 必ず閉じる。閉じないと一時ファイルがロックされて削除できなくなる
                # [EN] Must close; otherwise the temp file stays locked and cannot be deleted
                video.close()

    return await asyncio.to_thread(_extract)
