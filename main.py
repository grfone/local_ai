from src.installer import Installer
from src.runner import Run


def install():
    installer = Installer()
    installer.install_ollama()
    installer.download_model(auto_select_model=True)


def run():
    runner = Run()
    messages = [
    {"role": "user", "content": "My name is John."},
    {"role": "assistant", "content": "Nice to meet you, John!"},
    {"role": "user", "content": "What is my name?"},
    ]

    return runner.run(provider="Ollama", model="qwen3.5:4b", messages=messages)  # (provider="Ollama", model="qwen3.5:4b") or (provider="MiniMax", model="M3", messages=messages)


if __name__ == '__main__':
    install()
    print(run())