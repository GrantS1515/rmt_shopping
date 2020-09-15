from kivy.clock import Clock

from node import Quantity_Ingredient, Recipe_Node
from screen_utils import Screen_Button

class Recipe_Manager():

	def __init__(self, cookbook_data):
		self.cookbook_data = cookbook_data
		self.ingredient_name = None
		self.quantity_type = None
		self.quantity = None
		self.QI_list = []
		self.recipe_node = Recipe_Node(name='')

	@property
	def recipe_name(self):
		return recipe_node.name

	@recipe_name.setter
	def recipe_name(self, value):
		self.recipe_node.name = value

	def add_QI(self):
		self.QI_list.append(Quantity_Ingredient(self.quantity, self.quantity_type, self.ingredient_name))
		self.recipe_node.QI_list = self.QI_list
		self.recipe_node.update_observers()

		# reset so that we throw an error if something is not updated appropriately
		self.ingredient_name = None
		self.quantity_type = None
		self.quantity = None
		
	def add_recipe(self):

		if self.recipe_node.name == None:
			return

		self.cookbook_data.add(self.recipe_node)
		self.cookbook_data.save()

		# update
		self.cookbook_data.update_observers()

class Recipe_Manager_Screen_Button(Screen_Button):
	def __init__(self, screen_manager, screen_name, recipe_manager, **kwargs):
		super().__init__(screen_manager, screen_name, **kwargs)
		self.recipe_manager = recipe_manager

	def manager_action(self):
		raise NotImplementedError

	def on_press(self):
		self.manager_action()
		super().on_press()
