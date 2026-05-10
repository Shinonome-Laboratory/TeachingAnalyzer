# 🎓 TeachingAnalyzer

> 基于本地大模型的自监督微观教学行为挖掘与分析系统
> Self-supervised micro-teaching behavior mining and analysis powered by local LLMs
> ローカル LLM による自己教師あり微視的授業行動マイニング・分析システム

---

**切换语言 / Switch Language / 言語切替**
→ [🇨🇳 中文](#-中文说明) ｜ [🇺🇸 English](#-english) ｜ [🇯🇵 日本語](#-日本語)

---

## 🇨🇳 中文说明

### 项目介绍

TeachingAnalyzer 是一款面向教育研究者的本地化 AI 分析工具。  
上传一段教学录像，系统将自动完成以下全流程：

1. 从视频中提取音频
2. 使用 **Whisper** 进行语音转录，生成带时间戳的逐字稿
3. 调用本地 **Ollama** 大模型，对每一句话自动打上"教学行为标签"
4. 在前端以**散点图时序图**呈现完整的教学动作序列

所有数据均在本地处理，无需联网、无需上传至云端，充分保护隐私。

### 核心功能

| 功能 | 描述 |
|------|------|
| 微观行为识别 | 结合上下文，自动识别"激发认知冲突"、"确认前概念"等抽象教学动作 |
| 图影联动 | 点击时序图中的任意散点，视频自动跳转到对应时刻并播放 |
| 带时间戳逐字稿 | 以 `[MM:SS]` 格式展示完整的语音识别结果 |
| 一键导出 CSV | 导出兼容 Excel 的行为序列数据集（含 UTF-8 BOM，中文无乱码） |
| 多语言界面 | 支持中文 / English / 日本語，右上角一键切换 |

### 系统架构

```
┌─────────────────────────────────────────────┐
│              浏览器 (React 前端)              │
│   视频播放器  ←→  散点图  ←→  逐字稿/报告   │
└───────────────────┬─────────────────────────┘
                    │ HTTP POST /api/upload_and_analyze
┌───────────────────▼─────────────────────────┐
│           FastAPI 后端 (Python)              │
│                                             │
│  ① 保存视频到临时目录                        │
│  ② MoviePy + FFmpeg → 提取 WAV 音频         │
│  ③ OpenAI Whisper  → 带时间戳逐字稿         │
│  ④ Ollama (本地LLM) → 教学行为标签          │
│  ⑤ 清理临时文件，返回 JSON                  │
└─────────────────────────────────────────────┘

技术栈：
  前端  React 18 · Ant Design 5 · ECharts · i18next
  后端  FastAPI · Uvicorn · MoviePy · Whisper · Ollama
  本地  Ollama（LLM推理）· FFmpeg（音频处理）
```

### 前置要求

在运行本项目前，请确保已安装以下工具：

| 工具 | 要求 | 下载地址 |
|------|------|----------|
| Python | ≥ 3.9 | https://www.python.org |
| Node.js | ≥ 18 | https://nodejs.org |
| FFmpeg | 任意版本 | https://ffmpeg.org（Windows 推荐 `winget install ffmpeg`）|
| Ollama | 任意版本 | https://ollama.com |

### 使用方法（傻瓜式）

#### 第一步：克隆项目

```bash
git clone https://github.com/Shinonome-Laboratory/TeachingAnalyzer.git
cd TeachingAnalyzer
```

#### 第二步：拉取 Ollama 模型（至少选一个）

> 运行前请确保 Ollama 已在后台启动：`ollama serve`

| 模型 | 大小 | 适合场景 | 拉取命令 |
|------|------|----------|----------|
| Llama 3.1 (8B) | ~5 GB | 综合推荐，英文教学分析 | `ollama pull llama3.1:8b` |
| DeepSeek R1 (8B) | ~5 GB | 推理能力强，适合逻辑性强的课堂 | `ollama pull deepseek-r1:8b` |
| Qwen 3.5 (9B) | ~6 GB | 中文教学分析首选 | `ollama pull qwen3.5:9b` |
| Qwen 3.5 (2B) | ~2 GB | 低配置设备推荐 | `ollama pull qwen3.5:2b` |
| Phi-4 (14B) | ~9 GB | 高精度分析，需要较大显存 | `ollama pull phi4:14b` |
| Gemma 4 (E2B) | ~2 GB | 轻量高效 | `ollama pull gemma4:e2b` |
| GLM-4 Flash (9B) | ~6 GB | 中文理解优秀 | `ollama pull haervwe/GLM-4.6V-Flash-9B:latest` |

一键拉取所有模型（可选）：

```bash
ollama pull llama3.1:8b && ollama pull deepseek-r1:8b && ollama pull qwen3.5:9b && ollama pull qwen3.5:2b && ollama pull phi4:14b && ollama pull gemma4:e2b && ollama pull haervwe/GLM-4.6V-Flash-9B:latest
```

#### 第三步：自动配置环境

```bash
python setup.py
```

脚本将自动：
- 检查所有依赖工具
- 创建 Python 虚拟环境（`.venv`）
- 安装后端 pip 包（`backend/requirements.txt`）
- 安装前端 npm 包（`frontend/package.json`）

#### 第四步：启动项目

```bash
python start.py
```

启动后访问：**http://localhost:3000**

#### 第五步：使用界面

1. 在左侧面板选择 **Whisper 模型**（首次使用推荐 `base`）和 **Ollama 模型**
2. 将教学视频拖入上传区，点击上传
3. 等待处理完成（视频时长和机器性能决定时间，通常 1–5 分钟）
4. 点击散点图中的点，视频会自动跳转到对应时刻
5. 切换到「AI 深度分析」标签查看行为标签列表，可一键下载 CSV

---

## 🇺🇸 English

### Project Overview

TeachingAnalyzer is a privacy-first, fully local AI tool for educational researchers.  
Upload a teaching video and the system automatically runs the full pipeline:

1. Extract audio from the video
2. Transcribe it with **Whisper**, producing a timestamped transcript
3. Feed each sentence to a local **Ollama** LLM to generate a teaching behavior tag
4. Visualize the complete action sequence as an **interactive scatter-plot timeline**

Everything runs locally — no cloud uploads, no API keys required.

### Key Features

| Feature | Description |
|---------|-------------|
| Micro-behavior detection | Labels abstract teaching actions ("Create Cognitive Conflict", "Confirm Prior Knowledge") using context |
| Video–chart sync | Click any point on the timeline chart to jump to that exact moment in the video |
| Timestamped transcript | Full speech-to-text output in `[MM:SS]` format |
| One-click CSV export | Excel-compatible behavior sequence dataset with UTF-8 BOM |
| Multilingual UI | Chinese / English / Japanese — switch in the top-right corner |

### System Architecture

```
┌─────────────────────────────────────────────┐
│             Browser (React Frontend)         │
│   Video Player  ←→  Scatter Chart  ←→  Text │
└───────────────────┬─────────────────────────┘
                    │ HTTP POST /api/upload_and_analyze
┌───────────────────▼─────────────────────────┐
│            FastAPI Backend (Python)          │
│                                             │
│  ① Save video to temp directory             │
│  ② MoviePy + FFmpeg  → extract WAV audio   │
│  ③ OpenAI Whisper    → timestamped text     │
│  ④ Ollama (local LLM) → behavior tags       │
│  ⑤ Clean up temp files, return JSON         │
└─────────────────────────────────────────────┘

Stack:
  Frontend  React 18 · Ant Design 5 · ECharts · i18next
  Backend   FastAPI · Uvicorn · MoviePy · Whisper · Ollama
  Local     Ollama (LLM inference) · FFmpeg (audio processing)
```

### Prerequisites

| Tool | Requirement | Download |
|------|-------------|----------|
| Python | ≥ 3.9 | https://www.python.org |
| Node.js | ≥ 18 | https://nodejs.org |
| FFmpeg | any | https://ffmpeg.org (`winget install ffmpeg` on Windows) |
| Ollama | any | https://ollama.com |

### Step-by-Step Guide

#### Step 1 — Clone the repository

```bash
git clone https://github.com/Shinonome-Laboratory/TeachingAnalyzer.git
cd TeachingAnalyzer
```

#### Step 2 — Pull an Ollama model (pick at least one)

> Make sure Ollama is running first: `ollama serve`

| Model | Size | Best for | Pull command |
|-------|------|----------|--------------|
| Llama 3.1 (8B) | ~5 GB | General use, English classroom analysis | `ollama pull llama3.1:8b` |
| DeepSeek R1 (8B) | ~5 GB | Strong reasoning, logic-heavy lessons | `ollama pull deepseek-r1:8b` |
| Qwen 3.5 (9B) | ~6 GB | Best for Chinese classroom analysis | `ollama pull qwen3.5:9b` |
| Qwen 3.5 (2B) | ~2 GB | Low-spec devices | `ollama pull qwen3.5:2b` |
| Phi-4 (14B) | ~9 GB | High precision, requires more VRAM | `ollama pull phi4:14b` |
| Gemma 4 (E2B) | ~2 GB | Lightweight and efficient | `ollama pull gemma4:e2b` |
| GLM-4 Flash (9B) | ~6 GB | Excellent Chinese comprehension | `ollama pull haervwe/GLM-4.6V-Flash-9B:latest` |

Pull all models at once (optional):

```bash
ollama pull llama3.1:8b && ollama pull deepseek-r1:8b && ollama pull qwen3.5:9b && ollama pull qwen3.5:2b && ollama pull phi4:14b && ollama pull gemma4:e2b && ollama pull haervwe/GLM-4.6V-Flash-9B:latest
```

#### Step 3 — Set up the environment

```bash
python setup.py
```

This script will automatically:
- Verify all required tools
- Create a Python virtual environment (`.venv`)
- Install backend pip packages (`backend/requirements.txt`)
- Install frontend npm packages (`frontend/package.json`)

#### Step 4 — Launch the project

```bash
python start.py
```

Then open your browser at **http://localhost:3000**

#### Step 5 — Using the UI

1. In the left panel, choose a **Whisper model** (start with `base`) and an **Ollama model**
2. Drag and drop a teaching video into the upload zone
3. Wait for processing (typically 1–5 minutes depending on video length and hardware)
4. Click any point on the scatter chart — the video jumps to that timestamp
5. Switch to the "AI Deep Analysis" tab to see behavior tags; download as CSV with one click

---

## 🇯🇵 日本語

### プロジェクト概要

TeachingAnalyzer は、教育研究者向けのプライバシー重視の完全ローカル AI 分析ツールです。  
授業動画をアップロードすると、システムが自動でパイプライン全体を実行します：

1. 動画から音声を抽出
2. **Whisper** で音声をタイムスタンプ付きテキストに文字起こし
3. ローカル **Ollama** LLM が各文に授業行動ラベルを付与
4. **インタラクティブな散布図タイムライン**として動作シーケンスを可視化

すべてローカルで処理されます。クラウドへのアップロードも API キーも不要です。

### 主な機能

| 機能 | 説明 |
|------|------|
| 微視的行動検出 | 文脈を考慮し「認知的葛藤の生成」「前概念の確認」などの抽象的な授業行動を自動ラベル付け |
| 動画・チャート連動 | タイムラインの任意の点をクリックすると動画がその瞬間にジャンプ |
| タイムスタンプ付き文字起こし | `[MM:SS]` 形式の完全な音声認識結果 |
| ワンクリック CSV エクスポート | UTF-8 BOM 付き Excel 互換の行動シーケンスデータセット |
| 多言語 UI | 中国語 / English / 日本語 — 右上のセレクタで切り替え |

### システムアーキテクチャ

```
┌─────────────────────────────────────────────┐
│          ブラウザ（React フロントエンド）      │
│  動画プレーヤー ←→ 散布図 ←→ 文字起こし/レポート │
└───────────────────┬─────────────────────────┘
                    │ HTTP POST /api/upload_and_analyze
┌───────────────────▼─────────────────────────┐
│         FastAPI バックエンド（Python）        │
│                                             │
│  ① 動画を一時ディレクトリに保存              │
│  ② MoviePy + FFmpeg → WAV 音声を抽出        │
│  ③ OpenAI Whisper  → タイムスタンプ付き文字起こし │
│  ④ Ollama（ローカル LLM）→ 授業行動ラベル   │
│  ⑤ 一時ファイルを削除し JSON を返却          │
└─────────────────────────────────────────────┘

技術スタック：
  フロントエンド  React 18 · Ant Design 5 · ECharts · i18next
  バックエンド    FastAPI · Uvicorn · MoviePy · Whisper · Ollama
  ローカルツール  Ollama（LLM 推論）· FFmpeg（音声処理）
```

### 前提条件

| ツール | 要件 | ダウンロード |
|--------|------|-------------|
| Python | ≥ 3.9 | https://www.python.org |
| Node.js | ≥ 18 | https://nodejs.org |
| FFmpeg | 任意 | https://ffmpeg.org（Windows: `winget install ffmpeg`）|
| Ollama | 任意 | https://ollama.com |

### 手順ガイド

#### ステップ 1 — リポジトリをクローン

```bash
git clone https://github.com/Shinonome-Laboratory/TeachingAnalyzer.git
cd TeachingAnalyzer
```

#### ステップ 2 — Ollama モデルを取得（最低 1 つ）

> 先に Ollama を起動してください：`ollama serve`

| モデル | サイズ | 用途 | 取得コマンド |
|--------|--------|------|--------------|
| Llama 3.1 (8B) | ~5 GB | 汎用、英語授業分析に最適 | `ollama pull llama3.1:8b` |
| DeepSeek R1 (8B) | ~5 GB | 推論能力が高く、論理的な授業に向く | `ollama pull deepseek-r1:8b` |
| Qwen 3.5 (9B) | ~6 GB | 中国語授業分析に最適 | `ollama pull qwen3.5:9b` |
| Qwen 3.5 (2B) | ~2 GB | 低スペック端末向け | `ollama pull qwen3.5:2b` |
| Phi-4 (14B) | ~9 GB | 高精度、より多くの VRAM が必要 | `ollama pull phi4:14b` |
| Gemma 4 (E2B) | ~2 GB | 軽量かつ効率的 | `ollama pull gemma4:e2b` |
| GLM-4 Flash (9B) | ~6 GB | 中国語理解が優秀 | `ollama pull haervwe/GLM-4.6V-Flash-9B:latest` |

全モデルを一括取得（任意）：

```bash
ollama pull llama3.1:8b && ollama pull deepseek-r1:8b && ollama pull qwen3.5:9b && ollama pull qwen3.5:2b && ollama pull phi4:14b && ollama pull gemma4:e2b && ollama pull haervwe/GLM-4.6V-Flash-9B:latest
```

#### ステップ 3 — 環境を自動構築

```bash
python setup.py
```

このスクリプトが自動で実行します：
- 必要なツールの確認
- Python 仮想環境（`.venv`）の作成
- バックエンド pip パッケージのインストール（`backend/requirements.txt`）
- フロントエンド npm パッケージのインストール（`frontend/package.json`）

#### ステップ 4 — プロジェクトを起動

```bash
python start.py
```

ブラウザで **http://localhost:3000** を開いてください。

#### ステップ 5 — UI の使い方

1. 左パネルで **Whisper モデル**（初回は `base` を推奨）と **Ollama モデル**を選択
2. 授業動画をアップロードエリアにドラッグ＆ドロップ
3. 処理完了を待つ（動画の長さとマシン性能により 1〜5 分程度）
4. 散布図の任意の点をクリック → 動画がその時刻にジャンプ
5. 「AI 深層分析」タブで行動タグ一覧を確認、CSV でワンクリックダウンロード

---

## Project Structure / 项目结构 / プロジェクト構成

```
TeachingAnalyzer/
├── backend/
│   ├── main.py              # FastAPI 入口 / entry point / エントリーポイント
│   ├── config.py            # 全局配置 / global config / グローバル設定
│   ├── requirements.txt     # Python 依赖 / dependencies / 依存関係
│   └── services/
│       ├── video_service.py # 音频提取 / audio extraction / 音声抽出
│       ├── stt_service.py   # Whisper 语音识别 / STT / 音声認識
│       └── llm_service.py   # Ollama 行为分析 / behavior analysis / 行動分析
├── frontend/
│   ├── src/
│   │   ├── App.js           # 根组件 / root component / ルートコンポーネント
│   │   ├── locales/i18n.js  # 三语翻译 / translations / 三言語翻訳
│   │   └── components/
│   │       ├── VideoUploader.jsx
│   │       ├── VideoPlayer.jsx
│   │       ├── ScatterChart.jsx
│   │       └── EngineConfig.jsx
│   └── package.json
├── setup.py                 # 一键配置环境 / env setup / 環境構築
└── start.py                 # 一键启动 / one-click start / ワンクリック起動
```
