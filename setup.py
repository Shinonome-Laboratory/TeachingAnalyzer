"""
[ZH] TeachingAnalyzer 一键环境配置脚本
      克隆项目后运行本脚本，可自动完成：
        1. 检查 Python / Node.js / FFmpeg / Ollama 版本
        2. 创建 Python 虚拟环境 (.venv)
        3. 安装后端 pip 依赖 (backend/requirements.txt)
        4. 安装前端 npm 依赖 (frontend/package.json)
      用法：python setup.py

[JA] TeachingAnalyzer ワンクリック環境構築スクリプト
      プロジェクトをクローン後にこのスクリプトを実行すると以下を自動処理します：
        1. Python / Node.js / FFmpeg / Ollama のバージョン確認
        2. Python 仮想環境（.venv）の作成
        3. バックエンドの pip 依存関係のインストール（backend/requirements.txt）
        4. フロントエンドの npm 依存関係のインストール（frontend/package.json）
      使い方：python setup.py

[EN] TeachingAnalyzer one-click environment setup script
      Run this after cloning the project to automatically:
        1. Verify Python / Node.js / FFmpeg / Ollama versions
        2. Create a Python virtual environment (.venv)
        3. Install backend pip dependencies (backend/requirements.txt)
        4. Install frontend npm dependencies (frontend/package.json)
      Usage: python setup.py
"""

import os
import sys
import shutil
import subprocess
import venv

ROOT         = os.path.dirname(os.path.abspath(__file__))
VENV_DIR     = os.path.join(ROOT, ".venv")
REQUIREMENTS = os.path.join(ROOT, "backend", "requirements.txt")
FRONTEND_DIR = os.path.join(ROOT, "frontend")

IS_WINDOWS = sys.platform == "win32"

# [ZH] ANSI 颜色代码（Windows 10+ 终端支持）
# [JA] ANSI カラーコード（Windows 10+ ターミナル対応）
# [EN] ANSI color codes (supported by Windows 10+ terminals)
RESET  = "\033[0m"
BOLD   = "\033[1m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"


def enable_ansi():
    if IS_WINDOWS:
        os.system("")


def ok(msg):    print(f"  {GREEN}✔{RESET}  {msg}")
def warn(msg):  print(f"  {YELLOW}!{RESET}  {msg}")
def fail(msg):  print(f"  {RED}✘{RESET}  {msg}")
def info(msg):  print(f"  {CYAN}→{RESET}  {msg}")
def section(title):
    print(f"\n{BOLD}{YELLOW}[ {title} ]{RESET}")


# ---------------------------------------------------------------------------
# Helper: run a subprocess and return (returncode, stdout+stderr)
# ---------------------------------------------------------------------------
def run(cmd, cwd=None):
    result = subprocess.run(
        cmd, cwd=cwd,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", errors="replace",
    )
    return result.returncode, result.stdout.strip()


# ---------------------------------------------------------------------------
# Step 1 — Check required tools
# ---------------------------------------------------------------------------
def check_prerequisites():
    section("Step 1 / ステップ1 / 第一步 — Checking prerequisites")
    all_ok = True

    # Python version (need 3.9+)
    major, minor = sys.version_info.major, sys.version_info.minor
    ver_str = f"{major}.{minor}.{sys.version_info.micro}"
    if major == 3 and minor >= 9:
        ok(f"Python {ver_str}")
    else:
        fail(f"Python {ver_str} — requires Python 3.9 or higher")
        all_ok = False

    # Node.js / npm
    node_path = shutil.which("node")
    npm_path   = shutil.which("npm.cmd" if IS_WINDOWS else "npm")
    if node_path:
        _, node_ver = run(["node", "--version"])
        ok(f"Node.js {node_ver}")
    else:
        fail("Node.js not found — download from https://nodejs.org")
        all_ok = False

    if npm_path:
        npm_cmd = "npm.cmd" if IS_WINDOWS else "npm"
        _, npm_ver = run([npm_cmd, "--version"])
        ok(f"npm {npm_ver}")
    else:
        fail("npm not found — it is bundled with Node.js")
        all_ok = False

    # FFmpeg (required by MoviePy for audio extraction)
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        _, ffmpeg_ver = run(["ffmpeg", "-version"])
        first_line = ffmpeg_ver.splitlines()[0] if ffmpeg_ver else "unknown"
        ok(f"FFmpeg — {first_line}")
    else:
        warn("FFmpeg not found — audio extraction will fail at runtime")
        warn("  Windows: winget install ffmpeg   |   macOS: brew install ffmpeg   |   Linux: sudo apt install ffmpeg")
        # [ZH] FFmpeg 缺失不阻断安装流程，但运行时会出错
        # [JA] FFmpeg がなくてもセットアップは続行するが、実行時にエラーになる
        # [EN] Missing FFmpeg does not abort setup but will cause a runtime error

    # Ollama (required for LLM inference)
    ollama_path = shutil.which("ollama")
    if ollama_path:
        _, ollama_ver = run(["ollama", "--version"])
        ok(f"Ollama — {ollama_ver}")
    else:
        warn("Ollama not found — LLM analysis will fail at runtime")
        warn("  Download from https://ollama.com  and run:  ollama pull llama3.1:8b")

    return all_ok


# ---------------------------------------------------------------------------
# Step 2 — Create Python virtual environment
# ---------------------------------------------------------------------------
def create_venv():
    section("Step 2 / ステップ2 / 第二步 — Creating Python virtual environment (.venv)")

    if os.path.isdir(VENV_DIR):
        ok(f".venv already exists at {VENV_DIR} — skipping creation")
        return

    info("Creating .venv ...")
    venv.create(VENV_DIR, with_pip=True)
    ok(".venv created successfully")


# ---------------------------------------------------------------------------
# Step 3 — Install backend pip dependencies
# ---------------------------------------------------------------------------
def install_backend():
    section("Step 3 / ステップ3 / 第三步 — Installing backend pip dependencies")

    # [ZH] 直接调用 venv 内的 pip，无需激活虚拟环境
    # [JA] 仮想環境をアクティベートせずに venv 内の pip を直接呼び出す
    # [EN] Call the venv pip directly — no need to activate the virtualenv
    pip = (
        os.path.join(VENV_DIR, "Scripts", "pip.exe") if IS_WINDOWS
        else os.path.join(VENV_DIR, "bin", "pip")
    )

    if not os.path.isfile(pip):
        fail(f"pip not found at {pip} — virtual environment may be corrupt")
        return False

    info(f"Running: pip install -r backend/requirements.txt")
    code, out = run([pip, "install", "-r", REQUIREMENTS])
    if code == 0:
        ok("Backend dependencies installed")
    else:
        fail("pip install failed — see output below:")
        print(out)
        return False
    return True


# ---------------------------------------------------------------------------
# Step 4 — Install frontend npm dependencies
# ---------------------------------------------------------------------------
def install_frontend():
    section("Step 4 / ステップ4 / 第四步 — Installing frontend npm dependencies")

    npm_cmd = "npm.cmd" if IS_WINDOWS else "npm"
    if not shutil.which(npm_cmd):
        fail("npm not found — skipping frontend install")
        return False

    info("Running: npm install  (this may take a minute...)")
    code, out = run([npm_cmd, "install"], cwd=FRONTEND_DIR)
    if code == 0:
        ok("Frontend dependencies installed")
    else:
        fail("npm install failed — see output below:")
        print(out)
        return False
    return True


# ---------------------------------------------------------------------------
# Final summary
# ---------------------------------------------------------------------------
def print_summary(backend_ok, frontend_ok):
    section("Setup Summary / セットアップ概要 / 安装摘要")

    if backend_ok:
        ok("Backend ready")
    else:
        fail("Backend setup incomplete — check errors above")

    if frontend_ok:
        ok("Frontend ready")
    else:
        fail("Frontend setup incomplete — check errors above")

    if backend_ok and frontend_ok:
        print(f"""
{GREEN}{BOLD}All done! Start the project with:{RESET}

  {CYAN}python start.py{RESET}

{YELLOW}Note / 注意 / 備考:{RESET}
  • Make sure Ollama is running:   ollama serve
  • Pull a model if needed:        ollama pull llama3.1:8b
  • Make sure FFmpeg is on PATH
""")
    else:
        print(f"\n{YELLOW}Fix the errors above, then re-run:  python setup.py{RESET}\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main():
    enable_ansi()
    print(f"\n{BOLD}{YELLOW}{'='*55}{RESET}")
    print(f"{BOLD}{YELLOW}  TeachingAnalyzer — Environment Setup{RESET}")
    print(f"{BOLD}{YELLOW}{'='*55}{RESET}")

    prereq_ok   = check_prerequisites()
    if not prereq_ok:
        print(f"\n{RED}Critical prerequisites are missing. Please install them and re-run.{RESET}\n")
        sys.exit(1)

    create_venv()
    backend_ok  = install_backend()
    frontend_ok = install_frontend()
    print_summary(backend_ok, frontend_ok)


if __name__ == "__main__":
    main()
