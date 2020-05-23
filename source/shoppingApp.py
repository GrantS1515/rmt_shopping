import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.uix.screenmanager import FallOutTransition

from ingredients import IngredientsScreen

Builder.load_file('ingredients.kv')

class Shopping(ScreenManager):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.transition = FallOutTransition()

class ShoppingApp(App):
	def build(self):
		return Shopping()

if __name__ == '__main__':
	ShoppingApp().run()