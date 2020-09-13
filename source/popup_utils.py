from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput

from node import Node

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

class Add_Ingredient_Layout(RelativeLayout):

	loaded = False

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		kwargs = {'text': 'Enter Value', 'size_hint': (1, 0.1), 'pos_hint': {'center_y': 0.9}}
		self.text_input = TextInput(**kwargs)
		self.add_widget(self.text_input)

	def _get_add_button(self):
		raise NotImplementedError

	def _get_cancel_button(self):
		raise NotImplementedError

	def load_layout(self, **kwargs):
		'''
		Call only once
		'''
		if self.loaded:
			return

		self.add_widget(self._get_add_button())
		self.add_widget(self._get_cancel_button())

		self.loaded = True

class Add_Ingredient_Layout_Scaffold(Add_Ingredient_Layout):
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		

	def load_layout(self, tree_view, ingredient_data, popup, **kwargs):
		self.tree_view = tree_view
		self.ingredient_data = ingredient_data
		self.popup = popup

		super().load_layout(**kwargs)

	def _get_add_button(self):
		kwargs = {'text': 'Ok', 'size_hint': (0.3, 0.2), 'pos_hint': {'y': 0, 'right': 1}}
		return Add_Ingredient_Button_Scaffold(self.tree_view, self.ingredient_data, self.text_input, self.popup, **kwargs)

	def _get_cancel_button(self):
		kwargs = {'text': 'Cancel', 'size_hint': (0.3, 0.2), 'pos_hint': {'y': 0, 'x': 0}}
		return Dismiss_Popup(self.popup, **kwargs)

class Add_Ingredient_Button(Button):
	
	def __init__(self, tree_view, ingredient_data, text_input, popup, **kwargs):
		super().__init__(**kwargs)
		self.ingredient_data = ingredient_data
		self.tree_view = tree_view
		self.text_input = text_input
		self.popup = popup

	@staticmethod
	def _process_text(text):
		myText = text.lower()
		return myText[0].upper() + myText[1:]

	def get_node(self):
		raise NotImplementedError

	def get_kwargs_add(self):
		raise NotImplementedError

	def on_press(self):
		self.ingredient_data.add(self.get_node(), kwargs=self.get_kwargs_add())
		self.ingredient_data.save()
		self.ingredient_data.update_observers()
		self.popup.dismiss()


class Add_Ingredient_Button_Scaffold(Add_Ingredient_Button):
	def __init__(self, tree_view, ingredient_data, text_input,popup, **kwargs):
		super().__init__(tree_view, ingredient_data, text_input, popup, **kwargs)

	def get_node(self):
		text = self.text_input.text
		node_name = self._process_text(text)

		return Node(node_name)

	def get_kwargs_add(self):
		return {}