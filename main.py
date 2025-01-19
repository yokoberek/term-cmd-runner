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
                        on_enter=RunScriptAction("kitty"),
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
                    on_enter=RunScriptAction(f'kitty bash -c "{query}; exec bash"'),
                )
            ]
        )


if __name__ == "__main__":
    TerminalExtension().run()
