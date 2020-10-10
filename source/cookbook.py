from kivy.uix.screenmanager import Screen
from kivy.uix.relativelayout import RelativeLayout

from screen_utils import Screen_Selector, Screen_Button
from view import View_Nodes_Scroll
from popup_utils import Remove_From_Database_Button

class Cookbook_Home_Screen(Screen):
	def __init__(self, recipe_manager, cookbook_data, shopping_cookbook_data,screenmanager, **kwargs):
		super().__init__(**kwargs)
		self.name = 'Cookbook_Home_Screen'
		self.add_widget(Cookbook_Home_Layout(recipe_manager, cookbook_data, shopping_cookbook_data, screenmanager))

class Cookbook_Home_Layout(RelativeLayout):
	def __init__(self, recipe_manager, cookbook_data, shopping_cookbook_data, screenmanager, **kwargs):
		super().__init__(**kwargs)
		self.popups = []

		# add the view for recipes
		kwargs = {'size_hint': (1, 0.8), 'pos_hint': {'center_y': 0.5}}
		VD = View_Nodes_Scroll(cookbook_data, **kwargs)
		self.add_widget(VD)

		# add the buttons to add a new recipe
		kwargs = {'text': 'Add Recipe', 'size_hint': (0.3, 0.1), 'pos_hint': {'center_x': 0.5, 'y': 0}}
		SB = To_Recipe_Home(recipe_manager, screenmanager, 'Recipe_Home_Screen', **kwargs)
		# SB = Screen_Button(screenmanager, 'Recipe_Home_Screen', **kwargs)
		self.add_widget(SB)

		# add a button to remove recipe
		kwargs = {'text': 'Remove Recipe', 'size_hint': (0.3, 0.1), 'pos_hint': {'x': 0, 'y': 0}}
		RB = Remove_From_Database_Button(self, VD, cookbook_data, **kwargs)
		self.add_widget(RB)

		# add the button to switch main screens 
		kwargs = {'size_hint': (1, 0.1), 'pos_hint': {'top': 1}}
		selector = Screen_Selector(screenmanager, **kwargs)
		selector.recipe_screen_button.background_color = (0, 1, 0, 1)
		self.add_widget(selector)

		# add recipe to shopping list
		kwargs = {'text': 'To Shopping List', 'size_hint': (0.3, 0.1), 'pos_hint': {'right': 1, 'y': 0}}
		shopButton = Add_Shopping_Recipe_Button(cookbook_data, shopping_cookbook_data, screenmanager, 'Shopping_Cookbook_Screen', VD, **kwargs)
		self.add_widget(shopButton)

class Add_Shopping_Recipe_Button(Screen_Button):

	def __init__(self, cookbook_data, shopping_cookbook_data, screen_manager, screen_name, view_database, **kwargs):
		self.view_database = view_database
		self.cookbook_data = cookbook_data
		self.shopping_cookbook_data = shopping_cookbook_data
		super().__init__(screen_manager, screen_name, **kwargs)

	def on_press(self):
		node = self.view_database.my_selected_node

		if node != None:
			self.shopping_cookbook_data.add(node)
			self.shopping_cookbook_data.update_observers()
			super().on_press()

class To_Recipe_Home(Screen_Button):

	def __init__(self, recipe_manager, screen_manager, screen_name, **kwargs):
		super().__init__(screen_manager, screen_name, **kwargs)
		self.recipe_manager = recipe_manager

	def on_press(self):
		self.recipe_manager._reset_()
		super().on_press()