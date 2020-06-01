from kivy.uix.screenmanager import Screen
from kivy.uix.relativelayout import RelativeLayout
from view_database import View_Ingredient_Scaffold
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from database import Node
from add_ingredient_popup import Add_Ingredient_Layout_Scaffold

class IngredientsScreen(Screen):
	def __init__(self, ingredient_data, screenmanager, **kwargs):
		super().__init__(**kwargs)
		self.add_widget(IngredientLayout(ingredient_data, screenmanager))

class IngredientLayout(RelativeLayout):
	def __init__(self, ingredient_data, screenmanager, **kwargs):
		super().__init__(**kwargs)

		# setup the tree to view the database
		VD = View_Ingredient_Scaffold(ingredient_data)
		VD.update()
		self.add_widget(VD)

		# make the popup
		pop_layout = Add_Ingredient_Layout_Scaffold()
		add_pop = Popup(title='Add Ingredient', content=pop_layout, size_hint=(0.75, 0.75))
		pop_layout.load_layout(VD, ingredient_data, add_pop)

		# trigger the popup
		kwargs = {'text': 'Add Ingredient', 'size_hint': (0.5, 0.1), 'pos_hint': {'right': 1}}
		addButton = Launch_Popup(add_pop, **kwargs)
		self.add_widget(addButton)

		# remove button
		kwargs = {'text': 'Remove Ingredient', 'size_hint': (0.5, 0.1), 'pos_hint': {'x': 0, 'y': 0}}
		remButton = Remove_Ingredient(VD, ingredient_data, **kwargs)
		self.add_widget(remButton)

class Launch_Popup(Button):
	def __init__(self, popup, **kwargs):
		super().__init__(**kwargs)
		self.popup = popup

	def on_press(self):
		self.popup.open()

class Dismiss_Popup(Button):
	def __init__(self, popup, **kwargs):
		super().__init__(**kwargs)
		self.popup = popup

	def on_press(self):
		self.popup.dismiss()

class Remove_Ingredient(Button):
	def __init__(self, tree_view, ingredient_data, **kwargs):
		super().__init__(**kwargs)
		self.ingredient_data = ingredient_data
		self.tree_view = tree_view

	def on_press(self):
		tree_node = self.tree_view.selected_node
		if tree_node != None:
			if tree_node.text != 'Root':
				ingredient = self.ingredient_data.get_node(tree_node.text)
				self.ingredient_data.remove(ingredient)
				self.ingredient_data.save()
				self.ingredient_data.update_observers()