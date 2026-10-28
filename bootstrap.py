import sys
import subprocess

REQUIRED_PACKAGES = ["fastapi", "uvicorn", "pydantic", "requests", "numpy"]

def ensure_dependencies():
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package)
        except ImportError:
            print(f"[SELF-HEAL]: Missing '{package}'. Installing into environment...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"[SELF-HEAL]: Successfully installed '{package}'.")

if __name__ == "__main__":
    ensure_dependencies()
    print("[SYSTEM]: All workspace dependencies verified and active.")
