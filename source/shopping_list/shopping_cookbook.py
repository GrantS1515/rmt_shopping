from kivy.uix.screenmanager import Screen
from kivy.uix.relativelayout import RelativeLayout

import database.view as view
import database.node as nd
import utils.screen_utils as su

class Shopping_Cookbook_Screen(Screen):
	def __init__(self, shopping_cookbook_data, shop_quantity_data, screen_manager, **kwargs):
		super().__init__(**kwargs)
		self.name = 'Shopping_Cookbook_Screen'
		self.add_widget(Shopping_Cookbook_Layout(shopping_cookbook_data, shop_quantity_data, screen_manager))

class Shopping_Cookbook_Layout(RelativeLayout):
	def __init__(self, shopping_cookbook_data, shop_quantity_data, screen_manager, **kwargs):
		super().__init__(**kwargs)

		kwargs = {'size_hint': (1, 0.8), 'pos_hint': {'top': 1}}
		recipe_view = view.View_Nodes_Scroll(shopping_cookbook_data, **kwargs)
		self.add_widget(recipe_view)

		kwargs = {'text': 'Back To Cookbook', 'size_hint': (0.3, 0.1), 'pos_hint': {'y': 0, 'x': 0}}
		to_cookbook_button = su.Screen_Button(screen_manager, 'Cookbook_Home_Screen', **kwargs)
		self.add_widget(to_cookbook_button)

		kwargs = {'text': 'Quantities of Recipes', 'size_hint': (0.3, 0.1), 'pos_hint': {'y': 0, 'right': 1}}
		to_quantity_button = Shopping_Quantity_Button(screen_manager, 'Shopping_Quantity_Screen', shopping_cookbook_data, shop_quantity_data, **kwargs)
		self.add_widget(to_quantity_button)


class Shopping_Quantity_Button(su.Screen_Button):

	def __init__(self, screen_manager, screen_name, shopping_cookbook_data, shopping_quantity_data, **kwargs):
		self.shop_quantity_data = shopping_quantity_data
		self.shopping_cookbook_data = shopping_cookbook_data
		super().__init__(screen_manager, screen_name, **kwargs)

	def on_press(self):

		all_QI = []
		for recipe_node in self.shopping_cookbook_data:
			all_QI.extend(recipe_node.QI_list)

		red_nodes = nd.Node_Accumulator(all_QI)
		for QI_node in red_nodes:
			self.shop_quantity_data.add(QI_node)

		self.shop_quantity_data.update_observers()
		super().on_press()
		