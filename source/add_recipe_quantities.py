from kivy.uix.screenmanager import Screen
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput

from screen_utils import Screen_Button
from view import View_Nodes_Scroll
# from recipe_manager import Recipe_Manager_Screen_Button
from node import Quantity_Ingredient


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
		VQ = View_Nodes_Scroll(quantitiy_data, **kwargs)
		self.add_widget(VQ)

		# add to the recipe list
		kwargs = {'text': 'Finish Ingredient', 'size_hint': (0.5, 0.1), 'pos_hint': {'right': 1, 'bottom': 0}}
		addQuantity = Add_Quantity(screen_manager, 'Recipe_Home_Screen', recipe_manager, TI, VQ, **kwargs)
		self.add_widget(addQuantity)


class Add_Quantity(Screen_Button):
	def __init__(self, screen_manager, screen_name, recipe_manager, quantity_TI, view_database, **kwargs):
		super().__init__(screen_manager, screen_name, **kwargs)
		self.quantity_TI = quantity_TI
		self.view_database = view_database
		self.recipe_manager = recipe_manager

	def on_press(self):

		# TDOO write error catching for non-number quantity
		try:
			self.recipe_manager.quantity = float(self.quantity_TI.text)
		except Exception:
			return

		tree_node = self.view_database.my_selected_node
		if tree_node != None:
			self.recipe_manager.quantity_type = tree_node.name
			self.recipe_manager.add_QI()
			super().on_press()