import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.uix.screenmanager import FallOutTransition

from ingredients import Ingredients_Screen
from recipes import Recipe_Screen
from database import OD_Scaffold
from kivy.uix.button import Button
from quantities import Quantities_Screen
from recipes import Recipe_Screen
from add_recipe import Add_Recipe_Screen, Add_Recipe_Quantity_Screen

class Shopping(ScreenManager):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.transition = FallOutTransition()

		self.ingredient_name = None

		ingredient_data = OD_Scaffold('ingredients')
		self.add_widget(Ingredients_Screen(ingredient_data, self))
		
		quantities_data = OD_Scaffold('quantities')
		self.add_widget(Quantities_Screen(quantities_data, self))

		recipes_data = OD_Scaffold('recipes')
		self.add_widget(Recipe_Screen(recipes_data, self))

		self.add_widget(Add_Recipe_Screen(ingredient_data, self))

		self.add_widget(Add_Recipe_Quantity_Screen(quantities_data, self))

class ShoppingApp(App):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def build(self):
		return Shopping()

if __name__ == '__main__':
	ShoppingApp().run()