from langchain_core.messages import HumanMessage, AIMessage

from src.installer import Installer
from src.graph.graph import graph
from src.predictors import Predictor


def install():
    installer = Installer()
    installer.install_ollama()
    installer.download_model(auto_select_model=True)


def run():
    messages = []

    while True:
        user_input = input("You: ")

        if user_input.strip().lower() in ("exit", "quit"):
            break

        messages.append(
            HumanMessage(content=user_input)
        )

        result = graph.invoke(
            {
                "messages": messages,
                "status": "questioning",
                "final_prompt": None,
            }
        )

        messages = result["messages"]

        # Print the latest assistant response
        assistant_messages = [
            message
            for message in messages
            if isinstance(message, AIMessage)
        ]

        if assistant_messages:
            print("AI:", assistant_messages[-1].content)
        else:
            print("AI: No response was generated.")


if __name__ == '__main__':
    install()
    run()
