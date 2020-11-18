import kivy
kivy.require('1.9.0')

import sys, os
sys.path.insert(0, os.path.abspath('..'))

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import FallOutTransition
from kivy.uix.button import Button
from kivy.graphics import Rectangle

import database.database as db
import ingredients.ingredients as ig
import database.view as view
# import quantities.quantities as qt
# import add_recipe.recipe_manager as rm
# import add_recipe.add_recipe_home as arm
# import add_recipe.add_recipe_ingredients as ari
# import add_recipe.add_recipe_quantities as arq
# import cookbook.cookbook as cb
# import shopping_list.shopping_cookbook as sc
# import shopping_list.shopping_quantity as sq

class TestScreen(Screen):

	def __init__(self):
		super().__init__()
		ingredient_data = db.OD_Scaffold('ingredients')

		# kwargs = {'pos_hint': {'top': 0.9}}
		VD = view.View_Nodes_Scaffold(ingredient_data)
		# VD.pos_hint['y'] = 0.5
		# VD.do_layout()
		self.add_widget(VD)
		self.VD = VD

		kwargs = {'pos_hint': {'top': 1}, 'size_hint': (1, 0.1)}
		B = Button(text='Move Down', **kwargs)
		self.add_widget(B)
		B.bind(on_press=self.B_press)


	def B_press(self, instance):
		pass
		# print(self.VD.pos_hint)
		# self.VD.pos_hint['y'] = 0.2
		# self.VD.do_layout()
		# print(self.VD.pos_hint)




class Test(ScreenManager):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.transition = FallOutTransition()
		self.add_widget(TestScreen())
		# self.add_widget(ig.Ingredients_Screen(ingredient_data, self))

class TestApp(App):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def build(self):
		return Test()

if __name__ == '__main__':
	TestApp().run()