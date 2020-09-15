from kivy.uix.screenmanager import Screen
from kivy.uix.relativelayout import RelativeLayout

from screen_utils import Screen_Selector, Screen_Button
from view import View_Ingredient_Scaffold

class Cookbook_Home_Screen(Screen):
	def __init__(self, cookbook_data, screenmanager, **kwargs):
		super().__init__(**kwargs)
		self.name = 'Cookbook_Home_Screen'
		self.add_widget(Cookbook_Home_Layout(cookbook_data, screenmanager))

class Cookbook_Home_Layout(RelativeLayout):
	def __init__(self, cookbook_data, screenmanager, **kwargs):
		super().__init__(**kwargs)

		# add the view for recipes
		kwargs = {'size_hint': (1, 0.8), 'pos_hint': {'center_y': 0.5}}
		cookbook = View_Ingredient_Scaffold(cookbook_data, **kwargs)
		self.add_widget(cookbook)

		# add the buttons to add a new recipe
		kwargs = {'text': 'Add Recipe', 'size_hint': (0.3, 0.1), 'pos_hint': {'right': 1, 'y': 0}}
		SB = Screen_Button(screenmanager, 'Recipe_Home_Screen', **kwargs)
		self.add_widget(SB)

		# add a button to remove recipe

		# add the button to switch main screens 
		kwargs = {'size_hint': (1, 0.1), 'pos_hint': {'top': 1}}
		selector = Screen_Selector(screenmanager, **kwargs)
		selector.recipe_screen_button.background_color = (0, 1, 0, 1)
		self.add_widget(selector)

		# add recipe to shopping list
		kwargs = {'text': 'Add to Shopping', 'size_hint': (0.3, 0.1), 'pos_hint': {'center_x': 0.5, 'y': 0}}
		shopButton = Add_Shopping_Recipe_Button(screenmanager, 'Shopping_Cookbook_Screen', cookbook, **kwargs)
		self.add_widget(shopButton)

class Add_Shopping_Recipe_Button(Screen_Button):

	def __init__(self, screen_manager, screen_name, tree_view, **kwargs):
		self.tree_view = tree_view

		super().__init__(screen_manager, screen_name, **kwargs)

	def on_press(self):
		tree_node = self.tree_view.selected_node

		if tree_node != None:
			super().on_press()


