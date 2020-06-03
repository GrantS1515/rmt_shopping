from kivy.uix.screenmanager import Screen
from kivy.uix.relativelayout import RelativeLayout
from general_classes import Screen_Button
from view_database import View_Ingredient_Scaffold
from kivy.uix.textinput import TextInput
from database import Quantity_Ingredient

class Add_Recipe_Screen(Screen):
	def __init__(self, ingredient_data, screen_manager, **kwargs):
		super().__init__(**kwargs)
		self.name = 'Add_Recipe_Screen'
		self.add_widget(Add_Recipe_Layout(ingredient_data, screen_manager))

class Add_Recipe_Layout(RelativeLayout):
	def __init__(self, ingredient_data, screen_manager, **kwargs):
		super().__init__(**kwargs)

		# return to recipe screen
		kwargs = {'text': 'Back to Recipes', 'size_hint': (0.3, 0.1), 'pos_hint': {'top': 1, 'x': 0}}
		recipe_button = Screen_Button(screen_manager, 'Recipe_Screen', **kwargs)
		self.add_widget(recipe_button)

		# view of the ingredient list
		kwargs = {'size_hint': (1, 0.8), 'pos_hint': {'x': 0, 'center_y': 0.5}}
		VI = View_Ingredient_Scaffold(ingredient_data, **kwargs)
		self.add_widget(VI)
		
		# Add quantity
		kwargs = {'text': 'Next', 'size_hint': (0.5, 0.1), 'pos_hint': {'right': 1, 'y': 0}}
		LB = Load_Screen_Button(screen_manager, 'Add_Recipe_Quantity_Screen', VI, ingredient_data, **kwargs)
		self.add_widget(LB)

# class that will upload the current recipe list into a recipes observer when pressed

class Load_Screen_Button(Screen_Button):
	def __init__(self, screen_manager, screen_name, tree_view, observable_data, **kwargs):
		super().__init__(screen_manager, screen_name, **kwargs)
		self.tree_view = tree_view
		self.observable_data = observable_data

	def on_press(self):
		tree_node = self.tree_view.selected_node

		if tree_node != None:
			data_node = self.observable_data.get_node(tree_node.text)
			self.screen_manager.ingredient_name = data_node.name
			super().on_press()

class Add_Recipe_Quantity_Screen(Screen):
	def __init__(self, quantitiy_data, screen_manager, **kwargs):
		super().__init__(**kwargs)
		self.name = 'Add_Recipe_Quantity_Screen'
		self.layout = Add_Recipe_Quantity_Layout(quantitiy_data, screen_manager)
		self.add_widget(self.layout)


class Add_Recipe_Quantity_Layout(RelativeLayout):
	def __init__(self, quantitiy_data, screen_manager, **kwargs):
		super().__init__(**kwargs)
		self.data = None

		# return to recipe screen
		kwargs = {'text': 'Back to Ingredients', 'size_hint': (0.3, 0.1), 'pos_hint': {'top': 1, 'x': 0}}
		ingredient_button = Screen_Button(screen_manager, 'Add_Recipe_Screen', **kwargs)
		self.add_widget(ingredient_button)

		# add the text input for number of a quantity
		kwargs = {'size_hint': (1, 0.1), 'pos_hint': {'top': 0.9}}
		TI = TextInput(text='Enter Value', **kwargs)
		self.add_widget(TI)

		# view of the ingredient list
		kwargs = {'size_hint': (1, 0.7), 'pos_hint': {'x': 0, 'top': 0.8}}
		VQ = View_Ingredient_Scaffold(quantitiy_data, **kwargs)
		self.add_widget(VQ)

		# add to database
		kwargs = {'text': 'Finish', 'size_hint': (0.5, 0.1), 'pos_hint': {'right': 1, 'y': 0}}

		print(self.data)
		add_data = Add_Recipe_Database_Button(screen_manager, 'Add_Recipe_Screen', TI, VQ, **kwargs)
		self.add_widget(add_data)

class Add_Recipe_Database_Button(Screen_Button):

	def __init__(self, screen_manager, screen_name, text_input, tree_view, **kwargs):
		super().__init__(screen_manager, screen_name, **kwargs)
		self.text_input = text_input
		self.quantity_tree_view = tree_view
		self.screen_manager = screen_manager


	def on_press(self):
		quantity_type = self.quantity_tree_view.selected_node
		quantity = self.text_input.text
		ingredient_name = self.screen_manager.ingredient_name

		if (quantity_type != None) and (quantity != '') and (ingredient_name != None):
			node = Quantity_Ingredient(quantity, quantity_type,ingredient_name)
			super().on_press()

