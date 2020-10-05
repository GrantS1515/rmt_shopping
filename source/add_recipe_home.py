from kivy.uix.screenmanager import Screen
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput

from recipe_manager import Recipe_Manager_Screen_Button
from view import View_Recipe_Node

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

		# view the current recipe
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