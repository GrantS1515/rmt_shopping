import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.screenmanager import Screen

from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

class Temp(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))

        for i in range(100):
            kwargs = {}
            my_custom = myLayout(**kwargs)
            layout.add_widget(my_custom)

        root = ScrollView(size_hint=(1, 0.8), pos_hint={'top': 1})
        root.add_widget(layout)

        self.add_widget(root)


class myLayout(RelativeLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint_y = None
        self.height = 40

        left_btn = Button(text='left', size_hint=(0.5, 1), pos_hint={'x': 0, 'y': 0})
        right_btn = Button(text='right', size_hint=(0.5, 1), pos_hint={'right': 1, 'y': 0})
        self.add_widget(left_btn)
        self.add_widget(right_btn)


class TempApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return Temp()

if __name__ == '__main__':
    TempApp().run()