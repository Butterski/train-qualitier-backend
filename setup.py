import subprocess
import os
import sys

def create_venv():
    subprocess.run([sys.executable, '-m', 'venv', 'venv'])

def install_dependencies():
    pip_path = os.path.join('venv', 'bin' if os.name != 'nt' else 'Scripts', 'pip')
    subprocess.run([pip_path, 'install', '-r', 'requirements.txt'])

def initialize_database():
    python_path = os.path.join('venv', 'bin' if os.name != 'nt' else 'Scripts', 'python')
    subprocess.run([python_path, os.path.join('app', 'db_init.py')])

def main():
    create_venv()
    install_dependencies()
    initialize_database()

if __name__ == "__main__":
    main()