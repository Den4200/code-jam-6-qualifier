import os

from kivy.app import App
from kivy.logger import Logger
from kivy.factory import Factory
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import DragBehavior
from kivy.uix.floatlayout import FloatLayout


class ImageInterface(Widget):
    pass


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class DynamicImage(DragBehavior, Image):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._kb = Window.request_keyboard(None, self)
        self._kb.bind(on_key_down=self.on_key_down)

        self._keys = {
            'left': ('x', -10),
            'right': ('x', 10),
            'up': ('y', 10),
            'down': ('y', -10),
            'w': ('size', 20),
            's': ('size', -20)
        }

    def on_key_down(self, kb, key, *args, **kwargs):
        try:
            pos = self._keys[key[1]]
        except KeyError:
            return

        if pos[0] == 'x':
            self.x += pos[1]

        elif pos[0] == 'y':
            self.y += pos[1]

        elif pos[0] == 'size':
            
            if (self.height <= 0 or self.width <= 0) and pos[1] < 0:
                return

            self.height += pos[1]
            self.width += pos[1]


class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load image", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        app = App.get_running_app()
        try:
            app.root.ids.dynimg.source = os.path.join(path, filename[0])
        except IndexError:
            Logger.info('filechooser: No file selected')
        else:
            app.root.ids.dynimg.reload()
        finally:
            self.dismiss_popup()


class Application(App):
    """The application class manages the lifecycle of your program, it
    has events like on_start, on_stop, etc.

    see https://kivy.org/doc/stable/api-kivy.app.html for more information.
    """
    pass


if __name__ == "__main__":
    Application().run()
