import os
import subprocess
import sys

def create_virtual_env():
    """Creates a virtual environment if it doesn't exist."""
    if os.path.exists(".venv"):
        print("Virtual environment '.venv' already exists.")
        return True

    print("Creating virtual environment '.venv'...")
    try:
        subprocess.check_call([sys.executable, "-m", "venv", ".venv"])
        print("Virtual environment created successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment: {e}")
        return False

def install_dependencies():
    """Installs dependencies from requirements.txt into the virtual environment."""
    if not os.path.exists(".venv"):
        print("Virtual environment not found. Please create it first.")
        return

    print("Installing dependencies...")
    pip_executable = os.path.join(".venv", "Scripts", "pip.exe")
    requirements_file = os.path.join("project", "requirements.txt")

    if not os.path.exists(requirements_file):
        print(f"Error: '{requirements_file}' not found.")
        return

    try:
        subprocess.check_call([pip_executable, "install", "-r", requirements_file])
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")

if __name__ == "__main__":
    if create_virtual_env():
        install_dependencies()
    print("\nSetup complete.")
