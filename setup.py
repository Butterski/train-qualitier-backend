import subprocess
import os
import sys


def create_venv():
    subprocess.run([sys.executable, "-m", "venv", "venv"])


def install_dependencies():
    pip_path = os.path.join("venv", "bin" if os.name != "nt" else "Scripts", "pip")
    subprocess.run([pip_path, "install", "-r", "requirements.txt"])


def main():
    create_venv()
    install_dependencies()
    db_dir = "./database"
    db_file = os.path.join(db_dir, "database.sqlite")
    os.makedirs(db_dir, exist_ok=True)
    if not os.path.exists(db_file):
        open(db_file, "w").close()


if __name__ == "__main__":
    main()
