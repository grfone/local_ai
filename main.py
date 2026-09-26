from src.installer import Installer
from src.cli.app import CLIApp


def install():
    installer = Installer()
    installer.install_ollama()
    installer.download_model(auto_select_model=True)


if __name__ == '__main__':
    install()
    CLIApp().run()

