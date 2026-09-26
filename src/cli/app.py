# src/cli/app.py

from src.cli.chat import Chat
from src.instances.manager import InstanceManager


class CLIApp:
    def __init__(self):
        self.instance_manager = InstanceManager()
        self.running = True

    def run(self) -> None:
        self._print_welcome()

        while self.running:
            choice = self._show_main_menu()

            if choice == "1":
                self._create_instance()

            elif choice == "2":
                self._continue_instance()

            elif choice == "3":
                self._quick_instance()

            elif choice == "4":
                self._delete_instance()

            elif choice == "5":
                self._exit()

            else:
                print("\nInvalid option. Please try again.")

    # ------------------------------------------------------------------
    # Main menu
    # ------------------------------------------------------------------

    def _show_main_menu(self) -> str:
        print("\n" + "=" * 50)
        print("Main Menu")
        print("=" * 50)
        print("1. Create new instance")
        print("2. Continue instance")
        print("3. Quick instance (RAM)")
        print("4. Delete instance")
        print("5. Exit")
        print("=" * 50)

        return input("Select an option: ").strip()

    # ------------------------------------------------------------------
    # Instance creation
    # ------------------------------------------------------------------

    def _create_instance(self) -> None:
        print("\n" + "=" * 50)
        print("Create New Instance")
        print("=" * 50)

        name = self._read_instance_name()

        instance = self.instance_manager.create(
            name=name,
            persistent=True,
        )

        self._print_instance_info(instance)
        self._start_chat(instance)

    # ------------------------------------------------------------------
    # Existing instance
    # ------------------------------------------------------------------

    def _continue_instance(self) -> None:
        print("\n" + "=" * 50)
        print("Continue Instance")
        print("=" * 50)

        instances = self.instance_manager.list()

        if not instances:
            print("\nNo persistent instances found.")
            input("\nPress Enter to return to the menu...")
            return

        instance = self._select_instance(instances)

        if instance is None:
            return

        print(f"\nLoading instance '{instance.name}'...")

        self._start_chat(instance)

    # ------------------------------------------------------------------
    # Temporary instance
    # ------------------------------------------------------------------

    def _quick_instance(self) -> None:
        print("\n" + "=" * 50)
        print("Quick Instance")
        print("=" * 50)

        print(
            "\nThis instance exists only in RAM and will be lost "
            "when the application exits."
        )

        name = self._read_instance_name(
            default="quick-session"
        )

        instance = self.instance_manager.create(
            name=name,
            persistent=False,
        )

        self._print_instance_info(instance)
        self._start_chat(instance)

    # ------------------------------------------------------------------
    # Delete instance
    # ------------------------------------------------------------------

    def _delete_instance(self) -> None:
        print("\n" + "=" * 50)
        print("Delete Instance")
        print("=" * 50)

        instances = self.instance_manager.list()

        if not instances:
            print("\nNo persistent instances found.")
            input("\nPress Enter to return to the menu...")
            return

        instance = self._select_instance(instances)

        if instance is None:
            return

        print()
        print(f"Instance: {instance.name}")
        print(f"ID:       {instance.id}")

        confirmation = input(
            "\nAre you sure you want to delete this instance? "
            "[y/N]: "
        ).strip().lower()

        if confirmation not in {"y", "yes"}:
            print("\nDeletion cancelled.")
            return

        self.instance_manager.delete(instance.id)

        print(f"\nInstance '{instance.name}' deleted.")

    # ------------------------------------------------------------------
    # Chat
    # ------------------------------------------------------------------

    def _start_chat(self, instance) -> None:
        print("\nStarting chat...")
        print("Type 'exit' or 'quit' to return to the main menu.")

        chat = Chat(
            instance=instance,
        )

        chat.run()

    # ------------------------------------------------------------------
    # Instance selection
    # ------------------------------------------------------------------

    def _select_instance(self, instances):
        while True:
            print()

            for index, instance in enumerate(instances, start=1):
                print(
                    f"{index}. "
                    f"{instance.name} "
                    f"(updated: {instance.updated_at})"
                )

            print("0. Back")

            choice = input("\nSelect an instance: ").strip()

            if choice == "0":
                return None

            try:
                index = int(choice) - 1

                if 0 <= index < len(instances):
                    return instances[index]

            except ValueError:
                pass

            print("\nInvalid selection. Please try again.")

    # ------------------------------------------------------------------
    # Input helpers
    # ------------------------------------------------------------------

    def _read_instance_name(
        self,
        default: str | None = None,
    ) -> str:
        while True:
            if default:
                prompt = f"Instance name [{default}]: "
            else:
                prompt = "Instance name: "

            name = input(prompt).strip()

            if name:
                return name

            if default:
                return default

            print("Instance name cannot be empty.")

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def _print_instance_info(self, instance) -> None:
        print("\n" + "=" * 50)
        print("Instance ready")
        print("=" * 50)
        print(f"Name:         {instance.name}")
        print(f"ID:           {instance.id}")
        print(f"Thread:       {instance.thread_id}")
        print(
            "Persistence:  "
            f"{'long-term' if instance.persistent else 'RAM only'}"
        )
        print("=" * 50)

    def _print_welcome(self) -> None:
        print("\n" + "=" * 50)
        print("                 Agent CLI")
        print("=" * 50)

    def _exit(self) -> None:
        print("\nGoodbye!")
        self.running = False
