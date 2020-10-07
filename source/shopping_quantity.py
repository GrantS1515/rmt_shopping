from kivy.uix.screenmanager import Screen
from kivy.uix.relativelayout import RelativeLayout
from view import View_Nodes_Scaffold
from screen_utils import Screen_Button

class Shopping_Quantity_Screen(Screen):
	def __init__(self, shopping_quantity_data, screen_manager, **kwargs):
		super().__init__(**kwargs)
		self.name = 'Shopping_Quantity_Screen'
		self.add_widget(Shopping_Quantity_Layout(shopping_quantity_data, screen_manager))

class Shopping_Quantity_Layout(RelativeLayout):
	def __init__(self, shopping_quantity_data, screen_manager, **kwargs):
		super().__init__(**kwargs)

		kwargs = {'size_hint': (1, 0.8), 'pos_hint': {'top': 1}}

		recipe_view = View_Nodes_Scaffold(shopping_quantity_data, **kwargs)
		self.add_widget(recipe_view)

		kwargs = {'text': 'Back to Shopping Cookbook', 'size_hint': (0.3, 0.1), 'pos_hint': {'y': 0, 'x': 0}}
		to_cookbook_button = Screen_Button(screen_manager, 'Shopping_Cookbook_Screen', **kwargs)
		self.add_widget(to_cookbook_button)