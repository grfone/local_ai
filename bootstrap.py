import shutil
import subprocess
from pathlib import Path


UV_INSTALL_URL_UNIX = "https://astral.sh/uv/install.sh"


def find_uv():
    """Return the path to uv if it is installed, otherwise None."""
    uv = shutil.which("uv")
    if uv:
        return uv

    # The official installer installs uv in this directory by default.
    uv_path = Path.home() / ".local" / "bin" / "uv"

    if uv_path.exists():
        return str(uv_path)

    return None


def install_uv():
    """Install uv using Astral's official installer."""

    # If uv is already installed, then just exit this function
    if find_uv():
        return find_uv()

    # Else, install uv
    print("uv not found. Installing uv...")
    if shutil.which("curl"):  # using curl (doesn't come with ubuntu by default)
        subprocess.run(["sh","-c",f"curl -LsSf {UV_INSTALL_URL_UNIX} | sh",],check=True,)
    elif shutil.which("wget"):  # using wget (does come with ubuntu by default)
        subprocess.run(["sh","-c",f"wget -qO- {UV_INSTALL_URL_UNIX} | sh",],check=True,)
    else:
        raise RuntimeError("Could not install uv: neither curl nor wget is installed.")

    # Check the installation by finding the path
    uv = find_uv()
    if not uv:
        raise RuntimeError("uv was installed, but could not be found.")

    # Returns the path
    return uv


def sync_environment(uv):
    """Create/update the project's .venv using uv.lock."""
    print("Syncing Python environment...")

    # Since this is run from the root of this project, it detects the uv lock and toml in this folder (current folder)
    subprocess.run([uv, "sync"], check=True,)


def main():
    # Install uv
    uv = install_uv()

    # Sync the environment
    sync_environment(uv)
    print("Environment ready!")


if __name__ == "__main__":
    main()