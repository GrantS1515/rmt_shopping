import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.uix.screenmanager import FallOutTransition

from ingredients import IngredientsScreen
from database import OD_Scaffold

Builder.load_file('ingredients.kv')
# Builder.load_file('recipes.kv')

class Shopping(ScreenManager):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.transition = FallOutTransition()

		ingredient_data = OD_Scaffold('temp')
		self.add_widget(IngredientsScreen(ingredient_data, self))
		# self.add_widget(Recipe_Screen(self))

class ShoppingApp(App):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		# self.Ingredient_Tree = Shopping_Tree(Leaf, 'temp')

	def build(self):
		return Shopping()

if __name__ == '__main__':
	ShoppingApp().run()