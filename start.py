"""
[ZH] TeachingAnalyzer 一键启动脚本
      同时启动 FastAPI 后端（端口 8000）和 React 前端（端口 3000）
      用法：python start.py
[JA] TeachingAnalyzer ワンクリック起動スクリプト
      FastAPI バックエンド（ポート 8000）と React フロントエンド（ポート 3000）を同時起動する
      使い方：python start.py
[EN] TeachingAnalyzer one-click launcher
      Starts the FastAPI backend (port 8000) and React frontend (port 3000) simultaneously
      Usage: python start.py
"""

import os
import sys
import time
import subprocess
import threading

# [ZH] 项目根目录和前端目录的绝对路径
# [JA] プロジェクトルートとフロントエンドディレクトリの絶対パス
# [EN] Absolute paths to the project root and frontend directory
ROOT         = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(ROOT, "frontend")

IS_WINDOWS = sys.platform == "win32"

# [ZH] ANSI 终端颜色代码
# [JA] ANSI ターミナルカラーコード
# [EN] ANSI terminal color codes
RESET  = "\033[0m"
BOLD   = "\033[1m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
RED    = "\033[91m"


def enable_ansi():
    # [ZH] Windows 10+ 终端需要通过空系统调用激活 VT100 支持
    # [JA] Windows 10+ ターミナルは空のシステムコールで VT100 サポートを有効にする
    # [EN] Activate VT100 support on Windows 10+ terminals via an empty system call
    if IS_WINDOWS:
        os.system("")


def stream_output(proc: subprocess.Popen, label: str, color: str) -> None:
    # [ZH] 持续读取子进程的输出并以彩色标签打印，直到进程结束
    # [JA] プロセスが終了するまで子プロセスの出力を読み続け、カラーラベル付きで表示する
    # [EN] Continuously read the subprocess output and print it with a colored label until it exits
    for raw in iter(proc.stdout.readline, b""):
        text = raw.decode("utf-8", errors="replace").rstrip()
        if text:
            print(f"{color}{BOLD}[{label}]{RESET} {text}", flush=True)


def kill_tree(pid: int) -> None:
    # [ZH] 终止进程及其全部子进程（Windows 用 taskkill，Unix 用进程组信号）
    # [JA] プロセスとその全子プロセスを終了させる（Windows は taskkill、Unix はプロセスグループシグナル）
    # [EN] Kill the process and all its children (taskkill on Windows, process-group signal on Unix)
    if IS_WINDOWS:
        subprocess.call(
            ["taskkill", "/F", "/T", "/PID", str(pid)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        import signal
        try:
            os.killpg(os.getpgid(pid), signal.SIGTERM)
        except ProcessLookupError:
            pass


def start_backend() -> subprocess.Popen:
    # [ZH] 用当前 Python 解释器启动 uvicorn，确保使用同一虚拟环境
    # [JA] 現在の Python インタープリターで uvicorn を起動し、同一仮想環境を使用することを保証する
    # [EN] Launch uvicorn with the current Python interpreter to guarantee the same virtualenv is used
    cmd = [sys.executable, "-m", "uvicorn", "backend.main:app", "--reload", "--port", "8000"]
    kwargs = {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if IS_WINDOWS else {"start_new_session": True}
    return subprocess.Popen(
        cmd,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        **kwargs,
    )


def start_frontend() -> subprocess.Popen:
    # [ZH] Windows 下 npm 的实体是 npm.cmd，需要显式指定
    # [JA] Windows では npm の実体は npm.cmd のため、明示的に指定する必要がある
    # [EN] On Windows, npm is actually npm.cmd and must be specified explicitly
    npm = "npm.cmd" if IS_WINDOWS else "npm"
    kwargs = {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if IS_WINDOWS else {"start_new_session": True}
    return subprocess.Popen(
        [npm, "start"],
        cwd=FRONTEND_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        **kwargs,
    )


def main() -> None:
    enable_ansi()

    print(f"\n{YELLOW}{BOLD}{'='*50}{RESET}")
    print(f"{YELLOW}{BOLD}  TeachingAnalyzer — 一键启动 / One-click Start{RESET}")
    print(f"{YELLOW}{BOLD}{'='*50}{RESET}\n")

    print(f"{CYAN}{BOLD}[Backend]{RESET}  启动 FastAPI (http://localhost:8000)")
    backend_proc = start_backend()

    print(f"{GREEN}{BOLD}[Frontend]{RESET} 启动 React   (http://localhost:3000)")
    frontend_proc = start_frontend()

    # [ZH] 为每个进程启动独立的输出流线程（daemon=True 确保主进程退出时线程自动销毁）
    # [JA] 各プロセスに独立した出力ストリームスレッドを起動する（daemon=True でメインプロセス終了時に自動破棄）
    # [EN] Start a dedicated output-streaming thread per process (daemon=True ensures auto-cleanup on main exit)
    for proc, label, color in [
        (backend_proc,  "Backend",  CYAN),
        (frontend_proc, "Frontend", GREEN),
    ]:
        threading.Thread(target=stream_output, args=(proc, label, color), daemon=True).start()

    print(f"\n{YELLOW}两个服务均已启动，按 Ctrl+C 可同时停止所有服务。{RESET}\n")

    try:
        while True:
            # [ZH] 任一进程意外退出时，停止另一个并退出
            # [JA] どちらかのプロセスが予期せず終了した場合、もう一方を停止して終了する
            # [EN] If either process exits unexpectedly, stop the other one and exit
            if backend_proc.poll() is not None:
                print(f"\n{RED}[Backend] 进程已退出，正在停止前端...{RESET}")
                kill_tree(frontend_proc.pid)
                break
            if frontend_proc.poll() is not None:
                print(f"\n{RED}[Frontend] 进程已退出，正在停止后端...{RESET}")
                kill_tree(backend_proc.pid)
                break
            time.sleep(0.5)

    except KeyboardInterrupt:
        print(f"\n{YELLOW}收到 Ctrl+C，正在停止所有服务...{RESET}")
        for proc in [backend_proc, frontend_proc]:
            if proc.poll() is None:
                kill_tree(proc.pid)

    print(f"{YELLOW}所有服务已停止。{RESET}\n")


if __name__ == "__main__":
    main()
