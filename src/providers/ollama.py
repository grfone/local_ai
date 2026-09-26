import os
import subprocess
import time
import urllib.error
import urllib.request

from langchain_core.messages import BaseMessage
from langchain_ollama import ChatOllama

from src.models.model import Model


class OllamaModel(Model):

    def __init__(
        self,
        model: str = "qwen3.5:4b",
        host: str = "127.0.0.1",
        port: int = 11434,
    ):
        self.model = model
        self.host = host
        self.port = port

        self.project_root = os.getcwd()

        self.ollama_bin = os.path.join(
            self.project_root,
            "ollama",
            "bin",
            "ollama",
        )

        self.models_dir = os.path.join(
            self.project_root,
            "ollama_models",
        )

    def generate(
        self,
        messages: list[BaseMessage],
    ) -> str:
        self._start_server()

        llm = ChatOllama(
            model=self.model,
            base_url=f"http://{self.host}:{self.port}",
            num_predict=50000,
        )

        response = llm.invoke(messages)

        return str(response.content)

    def _start_server(self) -> None:
        env = os.environ.copy()
        env["OLLAMA_MODELS"] = self.models_dir

        try:
            urllib.request.urlopen(
                f"http://{self.host}:{self.port}/api/tags",
                timeout=1,
            )

            return

        except (
            urllib.error.URLError,
            TimeoutError,
        ):
            pass

        print("Starting Ollama server...")

        server = subprocess.Popen(
            [self.ollama_bin, "serve"],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        for _ in range(30):
            try:
                urllib.request.urlopen(
                    f"http://{self.host}:{self.port}/api/tags",
                    timeout=1,
                )

                print("Ollama server is ready.")

                return

            except (
                urllib.error.URLError,
                TimeoutError,
            ):
                time.sleep(1)

        server.terminate()

        raise RuntimeError(
            "Ollama server failed to start."
        )