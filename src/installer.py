import os
import subprocess
import json
import time
import urllib.request
import tarfile
import re
import html
import urllib.parse
import urllib.error
import zstandard as zstd


class Installer:
    def __init__(self):
        # Folders used in this class
        self.PROJECT_ROOT = os.getcwd()
        self.INSTALL_DIR = os.path.join(self.PROJECT_ROOT, 'ollama')
        self.MODELS_DIR = os.path.join(self.PROJECT_ROOT, 'ollama_models')


    def install_ollama(self):
        """Ollama installation"""

        # Check if ollama has been already installed
        ollama_bin = os.path.join(self.INSTALL_DIR, "bin", "ollama")
        if os.path.isfile(ollama_bin):
            return()

        # Create the directories, one for the binaries, another for the models.
        os.makedirs(self.INSTALL_DIR, exist_ok=True)
        os.makedirs(self.MODELS_DIR, exist_ok=True)

        # Point Ollama at our local models' folder.
        os.environ["OLLAMA_MODELS"] = str(self.MODELS_DIR)

        # Fetch the latest Ollama release for Linux amd64.
        api_url = "https://api.github.com/repos/ollama/ollama/releases/latest"
        req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())

        # Select the right asset.
        assets = {asset["name"]: asset["browser_download_url"] for asset in data["assets"]}
        asset_name = "ollama-linux-amd64.tar.zst"
        if asset_name not in assets:
            raise RuntimeError(f"Could not find '{asset_name}' in the latest Ollama release.")

        # Download it.
        download_url = assets[asset_name]
        archive_path = os.path.join(self.INSTALL_DIR,asset_name)
        print(f"Downloading Ollama from {download_url}...")
        urllib.request.urlretrieve(download_url, archive_path)

        # Extract the downloaded .tgz file.
        print("Extracting...")
        with open(archive_path, "rb") as compressed_file:
            dctx = zstd.ZstdDecompressor()
            with dctx.stream_reader(compressed_file) as reader:
                with tarfile.open(fileobj=reader, mode="r|") as tar_ref:
                    tar_ref.extractall(self.INSTALL_DIR, filter="data")

        # When you download a file from the internet, it may not have the executable permission set. Linux then refuses
        # to run it with "Permission denied". Setting it to 755 adds the execute bit.
        ollama_bin = os.path.join(self.INSTALL_DIR, "bin", "ollama")
        if not os.path.isfile(ollama_bin):  # Make sure extraction actually produced the Ollama binary.
            raise RuntimeError(f"Ollama binary was not found at: {ollama_bin}")
        os.chmod(ollama_bin, 0o755)
        print(f"Ollama installed at: {ollama_bin}")

        return None


    def download_model(self, auto_select_model=True):
        """Model installation"""

        # Check if the models were previously installed and skip installation if so.
        if os.path.isdir(self.MODELS_DIR):
            return()

        # 1. Start the Ollama server.
        env = os.environ.copy()
        env["OLLAMA_MODELS"] = str(self.MODELS_DIR)
        ollama_bin = os.path.join(self.INSTALL_DIR, "bin", "ollama")
        server = subprocess.Popen([ollama_bin, "serve"], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,)

        # 2. Wait until the server is ready.
        for _ in range(30):
            try:
                with urllib.request.urlopen("http://127.0.0.1:11434/api/tags",timeout=1):
                    break
            except(urllib.error.URLError, TimeoutError):
                time.sleep(1)
        else:  # The else block runs only if the loop finished without hitting a break.
            server.terminate()
            raise RuntimeError("Ollama server failed to start.")
        print("Ollama server is ready.")

        # 3. Let the user select a model.
        models = self._fetch_models()
        if auto_select_model:
            model = "qwen3.5:4b"
        else:
            while True:
                model = input("Enter the name of an Ollama model: ").strip()
                if model in models:
                    break
                print(f"Model '{model}' is not available in the Ollama library.")
                print("Please enter the name of one of the available models.")


        # 4. Check if the model is already installed.
        result = subprocess.run([ollama_bin, "list"], env=env, capture_output=True, text=True,)
        installed_models = result.stdout
        if model in installed_models:
            print(f"Model '{model}' is already installed.")
        else:
            # 5. Download the selected model.
            print(f"Downloading model: {model}...")
            result = subprocess.run([ollama_bin, "pull", model], env=env,)
            print(f"Model '{model}' is ready.")

        return None


    @staticmethod
    def _fetch_models():
        """Fetch the current models from the Ollama library."""

        # Declare the variables
        OLLAMA_LIBRARY_URL = "https://ollama.com/search"

        # Do the request
        request = urllib.request.Request(OLLAMA_LIBRARY_URL,headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(request) as response:
            page = response.read().decode("utf-8")

        # Find model links and add them to the list of models that we will return
        matches = re.findall(r'href=["\']/library/([^"\']+)["\']', page)
        models = []
        for model in matches:
            model = html.unescape(model)
            if model not in models:
                models.append(model)

        return models