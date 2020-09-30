from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput

from node import Node
from treeview_utils import Remove_From_TreeView

class Launch_Popup(Button):
	def __init__(self, popup, **kwargs):
		super().__init__(**kwargs)
		self.popup = popup

	def on_press(self):
		self.popup.open()

class PopLayout(RelativeLayout):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	@property
	def data_dict(self):
		raise NotImplementedError

class PopLayoutOkCancel(PopLayout):
	def __init__(self, screen_layout, okButton, buttonArgsDict, **kwargs):
		super().__init__(**kwargs)

		my_kwargs = {'text': 'Ok', 'size_hint': (0.5, 0.1), 'pos_hint': {'right': 1}}
		myOkButtton = okButton(**buttonArgsDict, **my_kwargs)
		self.add_widget(myOkButtton)

		my_kwargs = {'text': 'Cancel', 'size_hint': (0.5, 0.1), 'pos_hint': {'x': 0, 'y': 0}}
		cancelButton = Dismiss_Popup_from_Layout(screen_layout, **my_kwargs)
		self.add_widget(cancelButton)

class Add_Node_From_Popup(Button):

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
		
		for p in self.screen_layout.popups:
			p.dismiss()

class Remove_From_TreeView_Popup(Remove_From_TreeView):

	def __init__(self, screen_layout, tree_view, observer_database, **kwargs):
		
		super().__init__(tree_view, observer_database, **kwargs)
		self.screen_layout = screen_layout

	def on_press(self):
		super().on_press()
		for p in self.screen_layout.popups:
			p.dismiss()

class Dismiss_Popup_from_Layout(Button):
	def __init__(self, screen_layout, **kwargs):
		super().__init__(**kwargs)
		self.screen_layout = screen_layout

	def on_press(self):
		for p in self.screen_layout.popups:
			p.dismiss()