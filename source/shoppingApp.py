import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import FallOutTransition
import os 

import database.database as db
import database.database_lib as dbl
import ingredients.ingredients as ig
import quantities.quantities as qt
import add_recipe.recipe_manager as rm
import add_recipe.add_recipe_home as arm
import add_recipe.add_recipe_ingredients as ari
import add_recipe.add_recipe_quantities as arq
import cookbook.cookbook as cb
import shopping_list.shopping_cookbook as sc
import shopping_list.shopping_quantity as sq


class Shopping(ScreenManager):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.transition = FallOutTransition()

		ingredient_data = db.OD_Scaffold('ingredients.json')
		self.add_widget(ig.Ingredients_Screen(ingredient_data, self))
		
		quantities_data = db.OD_Scaffold('quantities.json')
		self.add_widget(qt.Quantities_Screen(quantities_data, self))

		cookbook_data = db.OD_Scaffold('cookbook.json')

		cookbook_data.attach_core(ingredient_data, dbl.process_core_node_db, dbl.process_obs_recipe_ing)
		cookbook_data.attach_core(quantities_data, dbl.process_core_node_db, dbl.process_obs_recipe_qtype)
		
		shop_cook_filename = 'shopping_cookbook.json'
		if os.path.exists(shop_cook_filename):
			os.remove(shop_cook_filename)
		shopping_cookbook_data = db.OD_Scaffold(shop_cook_filename)

		RM = rm.Recipe_Manager(cookbook_data)

		self.add_widget(cb.Cookbook_Home_Screen(RM, cookbook_data, shopping_cookbook_data, self))

		self.add_widget(arm.Recipe_Home_Screen(self, RM))

		self.add_widget(ari.Ingredients_Select_Screen(ingredient_data, self, RM))

		self.add_widget(arq.Quantity_Select_Screen(quantities_data, self, RM))

		shop_quantity_filename = 'shopping_quantity.json'
		if os.path.exists(shop_quantity_filename):
			os.remove(shop_quantity_filename)
		shop_quantity_data = db.OD_Scaffold(shop_quantity_filename)

		self.add_widget(sc.Shopping_Cookbook_Screen(shopping_cookbook_data, shop_quantity_data, self))

		self.add_widget(sq.Shopping_Quantity_Screen(shop_quantity_data, self))

class ShoppingApp(App):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def build(self):
		return Shopping()

if __name__ == '__main__':
	ShoppingApp().run()