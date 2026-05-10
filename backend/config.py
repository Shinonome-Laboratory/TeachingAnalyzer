import os

# [ZH] 计算项目根目录（此文件位于 backend/，所以向上两级）
# [JA] プロジェクトルートディレクトリを算出する（このファイルは backend/ 直下なので2段上）
# [EN] Resolve project root (this file lives under backend/, so go two levels up)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

# [ZH] 确保上传目录存在，不存在时自动创建
# [JA] アップロードディレクトリが存在しない場合は自動作成する
# [EN] Create the upload directory if it does not already exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

# [ZH] Whisper 语音识别配置
# [JA] Whisper 音声認識の設定
# [EN] Whisper speech-to-text configuration
STT_CONFIG = {
    "default_model": "base",  # [ZH] 可选: tiny, base, small, medium, large | [JA] 選択肢: tiny, base, small, medium, large | [EN] Options: tiny, base, small, medium, large
    "device": "cpu"           # [ZH] 有 GPU 时改为 "cuda" | [JA] GPU がある場合は "cuda" に変更 | [EN] Change to "cuda" if a GPU is available
}

# [ZH] Ollama 大模型配置
# [JA] Ollama LLM の設定
# [EN] Ollama large language model configuration
LLM_CONFIG = {
    "host": "http://localhost:11434",
    "default_model": "qwen2.5:7b",  # [ZH] 替换为本地实际部署的模型名称 | [JA] ローカルで実際に使用するモデル名に変更 | [EN] Replace with the model name deployed locally
    "temperature": 0.3
}
