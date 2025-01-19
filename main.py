import os
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
        # Determine the default terminal based on the system
        self.default_terminal = self.detect_default_terminal()

    def detect_default_terminal(self):
        # List of common terminal emulators to check
        terminals = [
            "gnome-terminal",
            "konsole",
            "xfce4-terminal",
            "xterm",
            "kitty",
            "alacritty",
        ]
        for terminal in terminals:
            if self.is_terminal_available(terminal):
                return terminal
        return "xterm"  # Fallback to xterm if no other terminal is found

    @staticmethod
    def is_terminal_available(terminal):
        return os.system(f"command -v {terminal} > /dev/null 2>&1") == 0


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or ""

        if not query:
            # If no command is entered, show placeholder
            return RenderResultListAction(
                [
                    ExtensionResultItem(
                        icon="images/icon.png",  # Adjust to your icon path
                        name="Enter terminal command",
                        description="Examples: ls, pwd, ps aux",
                        on_enter=RunScriptAction(extension.default_terminal),
                    )
                ]
            )

        # If command is entered, execute in terminal
        return RenderResultListAction(
            [
                ExtensionResultItem(
                    icon="images/icon.png",  # Adjust to your icon path
                    name=f"Run: {query}",
                    description=f'Execute "{query}" in terminal',
                    on_enter=RunScriptAction(
                        f'{extension.default_terminal} bash -c "{query}; exec bash"'
                    ),
                )
            ]
        )


if __name__ == "__main__":
    TerminalExtension().run()
