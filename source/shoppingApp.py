import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.uix.screenmanager import FallOutTransition
import os 

from database import OD_Scaffold
from ingredients import Ingredients_Screen
from quantities import Quantities_Screen
from cookbook import Cookbook_Home_Screen
from recipe_manager import Recipe_Manager
from add_recipe_home import Recipe_Home_Screen
from add_recipe_ingredients import Ingredients_Select_Screen
from add_recipe_quantities import Quantity_Select_Screen
from shopping_cookbook import Shopping_Cookbook_Screen

class Shopping(ScreenManager):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.transition = FallOutTransition()

		ingredient_data = OD_Scaffold('ingredients.json')
		self.add_widget(Ingredients_Screen(ingredient_data, self))
		
		quantities_data = OD_Scaffold('quantities.json')
		self.add_widget(Quantities_Screen(quantities_data, self))

		cookbook_data = OD_Scaffold('cookbook.json')

		shop_cook_filename = 'shopping_cookbook.json'
		if os.path.exists(shop_cook_filename):
			os.remove(shop_cook_filename)
		shop_cook_data = OD_Scaffold(shop_cook_filename)

		self.add_widget(Cookbook_Home_Screen(cookbook_data, self))

		RM = Recipe_Manager(cookbook_data)

		self.add_widget(Recipe_Home_Screen(self, RM))

		self.add_widget(Ingredients_Select_Screen(ingredient_data, self, RM))

		self.add_widget(Quantity_Select_Screen(quantities_data, self, RM))

		self.add_widget(Shopping_Cookbook_Screen(self))



class ShoppingApp(App):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def build(self):
		return Shopping()

if __name__ == '__main__':
	ShoppingApp().run()