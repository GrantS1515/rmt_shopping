import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.uix.screenmanager import FallOutTransition
import os 

from database import OD_Scaffold, is_consistent_ingredient_OD_recipe_node, is_consistent_quantity_type_OD_recipe_node
from ingredients import Ingredients_Screen
from quantities import Quantities_Screen
from cookbook import Cookbook_Home_Screen
from recipe_manager import Recipe_Manager
from add_recipe_home import Recipe_Home_Screen
from add_recipe_ingredients import Ingredients_Select_Screen
from add_recipe_quantities import Quantity_Select_Screen
from shopping_cookbook import Shopping_Cookbook_Screen
from shopping_quantity import Shopping_Quantity_Screen

class Shopping(ScreenManager):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.transition = FallOutTransition()

		ingredient_data = OD_Scaffold('ingredients.json')
		self.add_widget(Ingredients_Screen(ingredient_data, self))
		
		quantities_data = OD_Scaffold('quantities.json')
		self.add_widget(Quantities_Screen(quantities_data, self))

		cookbook_data = OD_Scaffold('cookbook.json')

		cookbook_data.attach_core(ingredient_data, is_consistent_ingredient_OD_recipe_node)
		cookbook_data.attach_core(quantities_data, is_consistent_quantity_type_OD_recipe_node)

		shop_cook_filename = 'shopping_cookbook.json'
		if os.path.exists(shop_cook_filename):
			os.remove(shop_cook_filename)
		shopping_cookbook_data = OD_Scaffold(shop_cook_filename)

		RM = Recipe_Manager(cookbook_data)

		self.add_widget(Cookbook_Home_Screen(RM, cookbook_data, shopping_cookbook_data, self))

		self.add_widget(Recipe_Home_Screen(self, RM))

		self.add_widget(Ingredients_Select_Screen(ingredient_data, self, RM))

		self.add_widget(Quantity_Select_Screen(quantities_data, self, RM))

		shop_quantity_filename = 'shopping_quantity.json'
		if os.path.exists(shop_quantity_filename):
			os.remove(shop_quantity_filename)
		shop_quantity_data = OD_Scaffold(shop_quantity_filename)

		self.add_widget(Shopping_Cookbook_Screen(shopping_cookbook_data, shop_quantity_data, self))

		self.add_widget(Shopping_Quantity_Screen(shop_quantity_data, self))

class ShoppingApp(App):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def build(self):
		return Shopping()

if __name__ == '__main__':
	ShoppingApp().run()