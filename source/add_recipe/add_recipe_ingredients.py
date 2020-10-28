from kivy.uix.screenmanager import Screen
from kivy.uix.relativelayout import RelativeLayout

import utils.screen_utils as su
import database.view as view

class Ingredients_Select_Screen(Screen):
	def __init__(self, ingredient_data, screen_manager, recipe_manager, **kwargs):
		super().__init__(**kwargs)
		self.name = 'Add_Recipe_Ingredients_Screen'
		self.add_widget(Ingredient_Select_Layout(ingredient_data, screen_manager, recipe_manager))

class Ingredient_Select_Layout(RelativeLayout):
	def __init__(self, ingredient_data, screen_manager, recipe_manager, **kwargs):
		super().__init__(**kwargs)

		# view all the ingredients list
		kwargs = {'size_hint': (1, 0.8), 'pos_hint': {'x': 0, 'top': 1}}
		VD = view.View_Nodes_Scroll(ingredient_data, **kwargs)
		self.add_widget(VD)

		kwargs = {'text': 'Add Ingredient', 'size_hint': (0.5, 0.1), 'pos_hint': {'right': 1, 'y': 0}}
		addButton = Add_Ingredient_Button(screen_manager, 'Add_Recipe_Quantity_Screen', recipe_manager, VD, **kwargs)
		self.add_widget(addButton)


class Add_Ingredient_Button(su.Screen_Button):

	def __init__(self, screen_manager, screen_name, recipe_manager, view_database, **kwargs):
		self.view_database = view_database
		self.recipe_manager = recipe_manager
		super().__init__(screen_manager, screen_name, **kwargs)
		

	def on_press(self):
		tree_node = self.view_database.my_selected_node

		if tree_node != None:
			self.recipe_manager.ingredient_name = tree_node.name
			super().on_press()