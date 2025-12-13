import subprocess
import sys

subprocess.run(
    [
        sys.executable, "-m",
        "streamlit", "run",
        "app/client/main.py"
    ],
    [
        sys.executable, "-m",
        "fastapi", "run",
        "app/server/main.py"
    ]
)
