import kivy
kivy.require('1.9.0')

import sys, os
sys.path.insert(0, os.path.abspath('..'))

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import FallOutTransition

import database.database as db
import ingredients.ingredients as ig
# import quantities.quantities as qt
# import add_recipe.recipe_manager as rm
# import add_recipe.add_recipe_home as arm
# import add_recipe.add_recipe_ingredients as ari
# import add_recipe.add_recipe_quantities as arq
# import cookbook.cookbook as cb
# import shopping_list.shopping_cookbook as sc
# import shopping_list.shopping_quantity as sq


class Test(ScreenManager):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.transition = FallOutTransition()

		ingredient_data = db.OD_Scaffold('ingredients.json')
		self.add_widget(ig.Ingredients_Screen(ingredient_data, self))

class TestApp(App):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def build(self):
		return Test()

if __name__ == '__main__':
	TestApp().run()