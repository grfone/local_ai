import os
import subprocess
import time
import urllib.error
import urllib.request

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

from src.models.messages import Message
from src.providers.base import BaseProvider


class OllamaProvider(BaseProvider):

    def __init__(
        self,
        model: str = "qwen3.5:4b",
        host: str = "127.0.0.1",
        port: int = 11434,
    ):
        self.model = model
        self.host = host
        self.port = port

        # Local Ollama installation
        self.project_root = os.getcwd()
        self.ollama_bin = os.path.join(
            self.project_root, "ollama", "bin", "ollama"
        )
        self.models_dir = os.path.join(
            self.project_root, "ollama_models"
        )

    def predict(self, messages: list[Message]) -> str:
        # Make sure Ollama is running
        self._start_server()

        llm = ChatOllama(
            model=self.model,
            base_url=f"http://{self.host}:{self.port}",
            num_predict=50000,
        )

        response = llm.invoke(
            self._to_langchain_messages(messages)
        )

        return response.content


    def _start_server(self):
        env = os.environ.copy()
        env["OLLAMA_MODELS"] = self.models_dir

        # Check if Ollama is already running
        try:
            urllib.request.urlopen(
                f"http://{self.host}:{self.port}/api/tags",
                timeout=1,
            )
            return
        except (urllib.error.URLError, TimeoutError):
            pass

        print("Starting Ollama server...")

        server = subprocess.Popen(
            [self.ollama_bin, "serve"],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # Wait for Ollama to become available
        for _ in range(30):
            try:
                urllib.request.urlopen(
                    f"http://{self.host}:{self.port}/api/tags",
                    timeout=1,
                )
                print("Ollama server is ready.")
                return
            except (urllib.error.URLError, TimeoutError):
                time.sleep(1)

        server.terminate()
        raise RuntimeError("Ollama server failed to start.")

    @staticmethod
    def _to_langchain_messages(messages: list[Message]):
        # Convert our messages to LangChain messages
        role_map = {
            "system": SystemMessage,
            "user": HumanMessage,
            "assistant": AIMessage,
        }

        return [
            role_map[message.role](content=message.content)
            for message in messages
        ]