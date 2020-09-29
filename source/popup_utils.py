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

class PopLayout(RelativeLayout):

	def __init__(self, screen_layout, observable_data, **kwargs):
		super().__init__(**kwargs)

	@property
	def data_dict(self):
		raise NotImplementedError

class PopLayoutOkCancel(PopLayout):

	def __init__(self, screen_layout, observable_data, add_from_popup, **kwargs):
		super().__init__(screen_layout, observable_data, **kwargs)

		kwargs = {'text': 'Ok', 'size_hint': (0.5, 0.1), 'pos_hint': {'right': 1}}
		okButton = add_from_popup(screen_layout, self, observable_data, **kwargs)
		self.add_widget(okButton)

		kwargs = {'text': 'Cancel', 'size_hint': (0.5, 0.1), 'pos_hint': {'x': 0, 'y': 0}}
		cancelButton = Dismiss_Popup_from_Layout(screen_layout, **kwargs)
		self.add_widget(cancelButton)

class Add_From_Popup(Button):

	def __init__(self, screen_layout, pop_layout, observable_data, **kwargs):
		super().__init__(**kwargs)
		self.observable_data = observable_data
		self.pop_layout = pop_layout
		self.screen_layout = screen_layout

	@property
	def my_node(self):
		raise NotImplementedError

	def on_press(self):
		self.observable_data.add(self.my_node)
		self.observable_data.save()
		self.screen_layout.popup.dismiss()


class Dismiss_Popup_from_Layout(Button):
	def __init__(self, screen_layout, **kwargs):
		super().__init__(**kwargs)
		self.screen_layout = screen_layout

	def on_press(self):
		self.screen_layout.popup.dismiss()