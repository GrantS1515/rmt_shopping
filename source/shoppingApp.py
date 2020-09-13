import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.uix.screenmanager import FallOutTransition
from kivy.uix.button import Button

# database imports
from database import OD_Scaffold
from ingredients import Ingredients_Screen


from quantities import Quantities_Screen
from cookbook import Cookbook_Home_Screen
from add_recipe import Ingredients_Select_Screen, Quantity_Select_Screen, Recipe_Home_Screen
from recipe_utils import Recipe_Manager

from add_recipe import Recipe_Home_Screen

class Shopping(ScreenManager):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.transition = FallOutTransition()

		ingredient_data = OD_Scaffold('ingredients.json')
		self.add_widget(Ingredients_Screen(ingredient_data, self))
		
		quantities_data = OD_Scaffold('quantities.json')
		self.add_widget(Quantities_Screen(quantities_data, self))

		cookbook_data = OD_Scaffold('cookbook.json')
		self.add_widget(Cookbook_Home_Screen(cookbook_data, self))


		RM = Recipe_Manager(cookbook_data)

		self.add_widget(Recipe_Home_Screen(self, RM))

		self.add_widget(Ingredients_Select_Screen(ingredient_data, self, RM))

		self.add_widget(Quantity_Select_Screen(quantities_data, self, RM))

class ShoppingApp(App):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def build(self):
		return Shopping()

if __name__ == '__main__':
	ShoppingApp().run()