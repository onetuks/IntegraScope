import os
import signal
import subprocess
import sys
import time


def start_fastapi():
    return subprocess.Popen(
        [
            sys.executable, "-m", "uvicorn",
            "app.server.main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload",
        ],
        preexec_fn=os.setsid,  # 프로세스 그룹 생성(종료 처리용)
    )


def start_streamlit():
    return subprocess.Popen(
        [
            sys.executable, "-m", "streamlit", "run",
            "client/main.py",
            "--server.port", "8501",
        ],
        preexec_fn=os.setsid,
    )


def terminate(proc: subprocess.Popen, name: str, timeout_sec: float = 5.0):
    if proc.poll() is not None:
        return

    try:
        # 그룹 전체에 SIGTERM
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        t0 = time.time()
        while time.time() - t0 < timeout_sec:
            if proc.poll() is not None:
                return
            time.sleep(0.1)

        # 안 죽으면 SIGKILL
        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
    except ProcessLookupError:
        pass


def main():
    api = start_fastapi()
    ui = start_streamlit()

    try:
        # 둘 중 하나라도 죽으면 같이 종료시키고 빠짐
        while True:
            if api.poll() is not None:
                raise RuntimeError(f"FastAPI exited with code {api.returncode}")
            if ui.poll() is not None:
                raise RuntimeError(f"Streamlit exited with code {ui.returncode}")
            time.sleep(0.3)

    except KeyboardInterrupt:
        # Stop/Ctrl+C 시 스택 없이 깔끔 종료
        pass
    finally:
        terminate(ui, "streamlit")
        terminate(api, "fastapi")


if __name__ == "__main__":
    main()
