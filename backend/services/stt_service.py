import asyncio
import importlib
from backend.config import STT_CONFIG

# [ZH] 全局缓存已加载的模型，避免每次请求都重新加载
# [JA] ロード済みモデルをグローバルにキャッシュし、リクエストごとの再ロードを防ぐ
# [EN] Cache the loaded model globally to avoid reloading on every request
_whisper_model = None
_current_model_name = None


def get_whisper_model(model_name: str = STT_CONFIG["default_model"]):
    """
    [ZH] 懒加载 Whisper 模型；若请求的模型与当前已加载的不同则重新加载
    [JA] Whisper モデルを遅延ロードし、要求されたモデルが異なる場合は再ロードする
    [EN] Lazy-load the Whisper model; reload if the requested model differs from the cached one
    """
    global _whisper_model, _current_model_name

    # [ZH] 模型未加载，或前端请求了不同的模型版本时重新加载
    # [JA] モデル未ロード、またはフロントエンドが別バージョンを要求した場合に再ロード
    # [EN] Reload when the model is not yet loaded or a different version is requested
    if _whisper_model is None or _current_model_name != model_name:
        try:
            whisper = importlib.import_module("whisper")
            print(f"正在加载 Whisper 模型 ({model_name})...")
            _whisper_model = whisper.load_model(model_name)
            _current_model_name = model_name
            print("Whisper 模型加载完成。")
        except ImportError:
            raise ImportError("未安装 whisper 库，请运行 pip install openai-whisper")
    return _whisper_model


async def transcribe_audio(audio_path: str, model_name: str = STT_CONFIG["default_model"]) -> dict:
    """
    [ZH] 在线程池中异步执行语音转文字，返回包含 text 和 segments 的字典
    [JA] スレッドプールで音声認識を非同期実行し、text と segments を含む辞書を返す
    [EN] Run speech-to-text asynchronously in a thread pool; returns a dict with text and segments
    """
    def _transcribe():
        model = get_whisper_model(model_name)
        # [ZH] 返回完整结果字典（包含 text 和带时间戳的 segments）
        # [JA] text とタイムスタンプ付き segments を含む完全な結果辞書を返す
        # [EN] Return the full result dict containing text and timestamped segments
        return model.transcribe(audio_path)

    return await asyncio.to_thread(_transcribe)
