import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.uix.screenmanager import FallOutTransition
from kivy.uix.button import Button

# database imports
from data.database import OD_Scaffold
from ingredients import Ingredients_Screen


from quantities import Quantities_Screen
from recipes import Cookbook_Home_Screen
from add_recipe import Add_Recipe_Ingredients_Screen, Add_Recipe_Quantity_Screen, Recipe_Home_Screen
from recipe_utils import Recipe_Manager
import os

class Temp_Add_Recipe(ScreenManager):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.transition = FallOutTransition()
		ingredient_data = OD_Scaffold('ingredients')
		quantities_data = OD_Scaffold('quantities')

		filename = 'cookbook'
		if os.path.exists(filename + '.data'):
			os.remove(filename + '.data')
		cookbook_data = OD_Scaffold(filename)

		self.add_widget(Cookbook_Home_Screen(cookbook_data, self))

		RM = Recipe_Manager(cookbook_data)

		RM.recipe_name = 'Waffles'
		RM.ingredient_name = 'Batter'
		RM.quantity_type = 'Oz'
		RM.quantity = 5
		RM.add_ingredient_quantity()
		# RM.add_recipe()

		self.add_widget(Recipe_Home_Screen(self, RM))

		self.current = 'Cookbook_Home_Screen'

class Temp_Add_Recipe_App(App):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def build(self):
		return Temp_Add_Recipe()

if __name__ == '__main__':
	Temp_Add_Recipe_App().run()