from kivy.uix.screenmanager import Screen
from kivy.uix.relativelayout import RelativeLayout
from general_classes import Screen_Button
from view_database import View_Ingredient_Scaffold, View_Recipe_Node
from kivy.uix.textinput import TextInput
from recipe_utils import Recipe_Manager_Screen_Button
from kivy.uix.label import Label

from database import Quantity_Ingredient
from kivy.uix.button import Button

class Recipe_Home_Screen(Screen):
	def __init__(self, screen_manager, recipe_manager, **kwargs):
		super().__init__(**kwargs)
		self.name = 'Recipe_Home_Screen'
		self.add_widget(Recipe_Home_Layout(screen_manager, recipe_manager))

class Recipe_Home_Layout(RelativeLayout):
	def __init__(self, screen_manager, recipe_manager, **kwargs):
		super().__init__(**kwargs)

		# return to cookbook screen
		kwargs = {'text': 'Save and Return to Recipes', 'size_hint': (0.3, 0.1), 'pos_hint': {'top': 1, 'x': 0}}
		cookbook_button = Cookbook_Home_Button(screen_manager, 'Cookbook_Home_Screen', recipe_manager, **kwargs)
		self.add_widget(cookbook_button)

		# the recipe naming screen
		kwargs = {'size_hint': (1, 0.1), 'pos_hint': {'top': 0.9}}
		TI_recipe_name = TextInput(text='Enter Recipe Name', **kwargs)
		self.add_widget(TI_recipe_name)

		# view the curren recipe
		kwargs = {'size_hint': (1, 0.7), 'pos_hint': {'center_y': 0.5}}
		vRecipe = View_Recipe_Node(recipe_manager.recipe_node, **kwargs)
		self.add_widget(vRecipe)

		# ingredients button
		kwargs = {'text': 'Add Ingredients', 'size_hint': (0.5, 0.1), 'pos_hint': {'right': 1, 'y': 0}}
		MIB = Modify_Ingredients_Button(screen_manager, 'Add_Recipe_Ingredients_Screen', recipe_manager, TI_recipe_name, **kwargs)
		self.add_widget(MIB)

class Cookbook_Home_Button(Recipe_Manager_Screen_Button):
	
	def __init__(self, screen_manager, screen_name, recipe_manager, **kwargs):
		super().__init__(screen_manager, screen_name, recipe_manager, **kwargs)

	def manager_action(self):
		self.recipe_manager.add_recipe()

class Modify_Ingredients_Button(Recipe_Manager_Screen_Button):
	def __init__(self, screen_manager, screen_name, recipe_manager, text_input, **kwargs):
		super().__init__(screen_manager, screen_name, recipe_manager, **kwargs)
		self.text_input = text_input
	
	def manager_action(self):
		self.recipe_manager.recipe_name = self.text_input.text

class Ingredients_Select_Screen(Screen):
	def __init__(self, ingredient_data, screen_manager, recipe_manager, **kwargs):
		super().__init__(**kwargs)
		self.name = 'Add_Recipe_Ingredients_Screen'
		self.add_widget(Ingredient_Select_Layout(ingredient_data, screen_manager, recipe_manager))

class Ingredient_Select_Layout(RelativeLayout):
	def __init__(self, ingredient_data, screen_manager, recipe_manager, **kwargs):
		super().__init__(**kwargs)

		# view all the ingredients list
		kwargs = {'size_hint': (1, 0.4), 'pos_hint': {'x': 0, 'top': 1}}
		VI = View_Ingredient_Scaffold(ingredient_data, **kwargs)
		self.add_widget(VI)

		kwargs = {'text': 'Add Ingredient', 'size_hint': (0.5, 0.1), 'pos_hint': {'right': 1, 'y': 0}}
		addButton = Add_Ingredient_Button(screen_manager, 'Add_Recipe_Quantity_Screen', recipe_manager, VI, **kwargs)
		self.add_widget(addButton)


class Add_Ingredient_Button(Screen_Button):

	def __init__(self, screen_manager, screen_name, recipe_manager, tree_view, **kwargs):
		self.tree_view = tree_view
		self.recipe_manager = recipe_manager
		super().__init__(screen_manager, screen_name, **kwargs)
		

	def on_press(self):
		tree_node = self.tree_view.selected_node

		if tree_node != None:
			self.recipe_manager.ingredient_name = tree_node.text
			super().on_press()

class Quantity_Select_Screen(Screen):
	def __init__(self, quantitiy_data, screen_manager, recipe_manager, **kwargs):
		super().__init__(**kwargs)
		self.name = 'Add_Recipe_Quantity_Screen'
		self.layout = Quantity_Select_Layout(quantitiy_data, screen_manager, recipe_manager, **kwargs)
		self.add_widget(self.layout)


class Quantity_Select_Layout(RelativeLayout):
	def __init__(self, quantitiy_data, screen_manager, recipe_manager, **kwargs):
		super().__init__(**kwargs)

		# add the text input for number of a quantity
		kwargs = {'size_hint': (0.5, 0.1), 'pos_hint': {'top': 1, 'right': 1}}
		TI = TextInput(text='Enter Numerical Value', **kwargs)
		self.add_widget(TI)

		# view of the quantities list
		kwargs = {'size_hint': (1, 0.9), 'pos_hint': {'x': 0, 'top': 0.9}}
		VQ = View_Ingredient_Scaffold(quantitiy_data, **kwargs)
		self.add_widget(VQ)

		# add to the recipe list
		kwargs = {'text': 'Finish Ingredient', 'size_hint': (0.5, 0.1), 'pos_hint': {'right': 1, 'bottom': 0}}
		addQuantity = Add_Quantity(screen_manager, 'Recipe_Home_Screen', recipe_manager, TI, VQ, **kwargs)
		self.add_widget(addQuantity)


class Add_Quantity(Screen_Button):
	def __init__(self, screen_manager, screen_name, recipe_manager, quantity_TI, quantity_tree, **kwargs):
		super().__init__(screen_manager, screen_name, **kwargs)
		self.quantity_TI = quantity_TI
		self.quantity_tree = quantity_tree
		self.recipe_manager = recipe_manager

	def on_press(self):

		# TDOO write error catching for non-number quantity
		try:
			self.recipe_manager.quantity = float(self.quantity_TI.text)
		except Exception:
			return

		tree_node = self.quantity_tree.selected_node
		if tree_node != None:
			self.recipe_manager.quantity_type = tree_node.text
			self.recipe_manager.add_QI()
			super().on_press()