import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout

from database import OD_Scaffold, Recipe_Scaffold, Quantity_Ingredient
from view_database import View_Ingredient_Scaffold, View_Recipe_Scaffold, View_Cookbook_Scaffold
import os


# temp
from kivy.uix.treeview import TreeView

class Temp(RelativeLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		# self.single_recipe()
		self.multiple_recipes()
		# ingredient_data = OD_Scaffold('temp')

	def multiple_recipes(self):

		myRecipes = OD_Scaffold('cookbook')

		filename = 'temp_recipe'

		if os.path.exists(filename + '.data'):
			os.remove(filename + '.data')
		
		RD1 = Recipe_Scaffold(filename, 'Western Omlet')
		pep = Quantity_Ingredient(1, 'number', 'pepper')
		eggs = Quantity_Ingredient(3, 'number', 'eggs')
		onion = Quantity_Ingredient(0.5, 'number', 'onion')
		RD1.add(pep)
		RD1.add(eggs)
		RD1.add(onion)

		RD2 = Recipe_Scaffold(filename, 'Waffles')
		eggs = Quantity_Ingredient(1, 'number', 'eggs')
		batter = Quantity_Ingredient(2, 'cup', 'batter')
		milk = Quantity_Ingredient(1, 'cup', 'milk')
		RD2.add(eggs)
		RD2.add(batter)
		RD2.add(onion)

		myRecipes.add(RD1)
		myRecipes.add(RD2)

		VC = View_Cookbook_Scaffold(myRecipes)
		myRecipes.update_observers()
		self.add_widget(VC)
	



	def single_recipe(self):

		filename = 'temp_recipe'

		if os.path.exists(filename + '.data'):
			os.remove(filename + '.data')
		
		RD = Recipe_Scaffold(filename, 'Western Omlet')

		pep = Quantity_Ingredient(1, 'number', 'pepper')
		eggs = Quantity_Ingredient(3, 'number', 'eggs')
		onion = Quantity_Ingredient(0.5, 'number', 'onion')

		RD.add(pep)
		RD.add(eggs)
		RD.add(onion)

		VR = View_Recipe_Scaffold(RD)
		RD.update_observers()

		self.add_widget(VR)

		

class TempApp(App):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def build(self):
		return Temp()

if __name__ == '__main__':
	TempApp().run()