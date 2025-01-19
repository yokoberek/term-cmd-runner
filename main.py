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
            # Jika tidak ada perintah, tampilkan placeholder
            return RenderResultListAction(
                [
                    ExtensionResultItem(
                        icon="images/icon.png",  # Sesuaikan dengan path icon Anda
                        name="Masukkan perintah terminal",
                        description="Contoh: ls, pwd, ps aux",
                        on_enter=RunScriptAction("kitty"),
                    )
                ]
            )

        # Jika ada perintah, jalankan di terminal
        return RenderResultListAction(
            [
                ExtensionResultItem(
                    icon="images/icon.png",  # Sesuaikan dengan path icon Anda
                    name=f"Jalankan: {query}",
                    description=f'Eksekusi "{query}" di terminal',
                    on_enter=RunScriptAction(f'kitty bash -c "{query}; exec bash"'),
                )
            ]
        )


if __name__ == "__main__":
    TerminalExtension().run()
