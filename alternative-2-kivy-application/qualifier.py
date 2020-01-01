from kivy.app import App
from kivy.lang import Builder


KV_RULES = """
Label:
    text: 'Hello world!'
"""


class Application(App):
    """The application class manages the lifecycle of your program, it
    has events like on_start, on_stop, etc.

    see https://kivy.org/doc/stable/api-kivy.app.html for more information.
    """

    def build(self):
        return Builder.load_string(KV_RULES)


if __name__ == "__main__":
    Application().run()
