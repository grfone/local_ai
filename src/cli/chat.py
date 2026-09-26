from __future__ import annotations

from langchain_core.messages import AIMessage, HumanMessage

from src.graph.graph import graph
from src.instances.instance import AgentInstance
from src.models.context import AgentContext
from src.providers.factory import ProviderFactory


class Chat:
    """
    Terminal chat interface for an existing agent instance.

    Chat owns the runtime model selection.

    The graph itself remains completely independent
    of the concrete model provider.
    """

    def __init__(
        self,
        instance: AgentInstance,
    ) -> None:
        self.instance = instance

        self.model = ProviderFactory.create()

        self.config = {
            "configurable": {
                "thread_id": instance.thread_id,
            }
        }

    def run(self) -> None:
        self._print_welcome_message()

        while True:
            try:
                user_input = self._read_input()

                if self._should_exit(user_input):
                    self._print_goodbye_message()
                    break

                if not user_input:
                    continue

                response = self._send_message(
                    user_input,
                )

                self._print_response(
                    response,
                )

            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break

            except EOFError:
                print("\n\nGoodbye!")
                break

            except Exception as exc:
                self._print_error(exc)

    def _read_input(self) -> str:
        return input("\nYou: ").strip()

    def _should_exit(
        self,
        user_input: str,
    ) -> bool:
        return user_input.lower() in {
            "exit",
            "quit",
        }

    def _send_message(
        self,
        user_input: str,
    ) -> str:
        result = graph.invoke(
            {
                "messages": [
                    HumanMessage(
                        content=user_input,
                    )
                ],
            },
            config=self.config,
            context=AgentContext(
                model=self.model,
            ),
        )

        return self._get_last_response(
            result,
        )

    def _get_last_response(
        self,
        result: dict,
    ) -> str:
        messages = result.get(
            "messages",
            [],
        )

        for message in reversed(messages):
            if isinstance(message, AIMessage):
                return self._normalize_content(
                    message.content,
                )

        return "No response was generated."

    def _normalize_content(
        self,
        content,
    ) -> str:
        if isinstance(content, str):
            return content

        if isinstance(content, list):
            parts: list[str] = []

            for item in content:
                if isinstance(item, str):
                    parts.append(item)

                elif isinstance(item, dict):
                    text = item.get("text")

                    if text:
                        parts.append(str(text))

            if parts:
                return "\n".join(parts)

        return str(content)

    def _print_welcome_message(self) -> None:
        print("\n" + "=" * 50)
        print(f"Instance: {self.instance.name}")
        print("=" * 50)
        print(
            "Type 'exit' or 'quit' "
            "to return to the main menu."
        )

    def _print_response(
        self,
        response: str,
    ) -> None:
        print(f"\nAI: {response}")

    def _print_error(
        self,
        error: Exception,
    ) -> None:
        print(
            f"\nAI: An error occurred: {error}"
        )

    def _print_goodbye_message(self) -> None:
        print(
            "\nReturning to main menu..."
        )
