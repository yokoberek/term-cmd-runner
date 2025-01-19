import os
import json
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction


class TerminalExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.history_file = os.path.expanduser(
            "~/.local/share/ulauncher/terminal_history.json"
        )
        self.load_history()

    def load_history(self):
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, "r") as f:
                    self.dir_history = json.load(f)
            else:
                self.dir_history = {"directories": []}
        except Exception:
            self.dir_history = {"directories": []}

    def save_history(self, directory):
        if directory not in self.dir_history["directories"]:
            self.dir_history["directories"].insert(0, directory)
            # Batasi history hingga 20 entri
            self.dir_history["directories"] = self.dir_history["directories"][:20]

            try:
                os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
                with open(self.history_file, "w") as f:
                    json.dump(self.dir_history, f)
            except Exception as e:
                print(f"Error saving history: {e}")


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or ""

        if not query:
            return RenderResultListAction(
                [
                    ExtensionResultItem(
                        icon="images/icon.png",
                        name="Masukkan perintah terminal",
                        description="Contoh: ls, pwd, cd [folder]",
                        on_enter=RunScriptAction("gnome-terminal"),
                    )
                ]
            )

        # Handle cd command dengan auto-complete
        if query.startswith("cd "):
            path_query = query[3:].strip()  # Hapus 'cd ' dari query
            items = []

            # Tambahkan sugesti dari history
            for dir_path in extension.dir_history["directories"]:
                if path_query.lower() in dir_path.lower():
                    items.append(
                        ExtensionResultItem(
                            icon="images/icon.png",
                            name=f"cd {dir_path}",
                            description=f"Buka direktori (dari history): {dir_path}",
                            on_enter=RunScriptAction(
                                f'gnome-terminal -- bash -c "cd {dir_path}; exec bash"'
                            ),
                        )
                    )

            # Cek direktori saat ini untuk sugesti
            try:
                current_dir = os.path.expanduser(
                    "~" if path_query.startswith("~") else path_query
                )
                base_dir = os.path.dirname(current_dir) if path_query else "."

                if os.path.isdir(base_dir):
                    for entry in os.listdir(base_dir):
                        full_path = os.path.join(base_dir, entry)
                        if os.path.isdir(full_path) and entry.lower().startswith(
                            os.path.basename(path_query).lower()
                        ):
                            items.append(
                                ExtensionResultItem(
                                    icon="images/icon.png",
                                    name=f"cd {full_path}",
                                    description=f"Buka direktori: {full_path}",
                                    on_enter=RunScriptAction(
                                        f'gnome-terminal -- bash -c "cd {full_path}; extension.save_history({full_path}); exec bash"'
                                    ),
                                )
                            )
            except Exception as e:
                print(f"Error scanning directory: {e}")

            if items:
                return RenderResultListAction(items[:8])  # Batasi hingga 8 sugesti

        # Default behavior untuk perintah non-cd
        return RenderResultListAction(
            [
                ExtensionResultItem(
                    icon="images/icon.png",
                    name=f"Jalankan: {query}",
                    description=f'Eksekusi "{query}" di terminal',
                    on_enter=RunScriptAction(
                        f'gnome-terminal -- bash -c "{query}; exec bash"'
                    ),
                )
            ]
        )


if __name__ == "__main__":
    TerminalExtension().run()
