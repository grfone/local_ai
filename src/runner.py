import os
import subprocess
import time
import urllib
import urllib.request
import urllib.error
import dotenv
import requests
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage


class Run:
    def __init__(self):
        self.PROJECT_ROOT = os.getcwd()
        self.OLLAMA_BIN = os.path.join(self.PROJECT_ROOT,"ollama","bin","ollama",)
        self.MODELS_DIR = os.path.join(self.PROJECT_ROOT,"ollama_models",)
        self.MODEL = ""
        self.OLLAMA_HOST = "127.0.0.1"
        self.OLLAMA_PORT = 11434
        self.MINIMAX_API_URL = "https://api.minimax.io/v1/text/chatcompletion_v2"
        self.MINIMAX_MODEL = ""
        dotenv.load_dotenv()
        self.MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY")


    def run(self, provider="Ollama", model="qwen3.5:4b", messages=""):
        self.MODEL = model
        answer = None


        if provider == "Ollama":
            ollama_messages = self._minimax_to_ollama_messages(messages)
            self._start_ollama_server()
            llm = ChatOllama(model="qwen3.5:4b", base_url=f"http://{self.OLLAMA_HOST}:{self.OLLAMA_PORT}", )
            response = llm.invoke(ollama_messages)
            answer = response.content

        elif provider == "MiniMax":
            self.MINIMAX_MODEL = f"{provider}-{model}"
            if not self.MINIMAX_API_KEY:
                raise RuntimeError("MINIMAX_API_KEY is missing. " "Add it to your .env file.")

            payload = {"model": self.MINIMAX_MODEL, "messages": messages, }
            response = requests.post(self.MINIMAX_API_URL, headers={"Authorization": f"Bearer {self.MINIMAX_API_KEY}",
                                                                    "Content-Type": "application/json", }, json=payload,timeout=120, )
            response.raise_for_status()
            data = response.json()
            answer = data["choices"][0]["message"]["content"]

        return answer


    def _start_ollama_server(self):
        """Start Ollama server."""

        # Ollama stores the models here.
        env = os.environ.copy()
        env["OLLAMA_MODELS"] = self.MODELS_DIR

        # Check whether an Ollama server is already running, so we don't stack process after process
        try:
            with urllib.request.urlopen(f"http://{self.OLLAMA_HOST}:{self.OLLAMA_PORT}/api/tags",timeout=1,):
                print("Ollama server is already running.")
                return None
        except (urllib.error.URLError, TimeoutError):
            pass

        # Start Ollama server
        print("Starting Ollama server...")
        server = subprocess.Popen([self.OLLAMA_BIN,"serve",], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,)

        # Wait for the server to become ready.
        for _ in range(30):
            try:
                with urllib.request.urlopen(f"http://{self.OLLAMA_HOST}:{self.OLLAMA_PORT}/api/tags",timeout=1,):
                    print("Ollama server is ready.")
                    return server
            except (urllib.error.URLError, TimeoutError):
                time.sleep(1)

        # If the server doesn't start.
        server.terminate()
        raise RuntimeError("Ollama server failed to start.")


    @staticmethod
    def _minimax_to_ollama_messages(messages):
        """Convert MiniMax/OpenAI-style messages to LangChain messages for Ollama."""

        # Role mapping, minimax (key) vs ollama (value)
        role_map = {"system": SystemMessage, "user": HumanMessage, "assistant": AIMessage, }

        # Transform the messages item by item in the messages list
        ollama_messages = []
        for message in messages:
            role = message["role"]
            content = message["content"]

            if role not in role_map:
                raise ValueError(f"Unsupported message role: {role}")

            ollama_messages.append(role_map[role](content=content))

        return ollama_messages