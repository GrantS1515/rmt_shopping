from kivy.uix.screenmanager import Screen
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

from view import View_Ingredient_Scaffold
from popup_utils import Launch_Popup, PopLayoutOkCancel, Add_Node_From_Popup, Remove_From_TreeView_Popup
# from treeview_utils import Remove_From_TreeView
from screen_utils import Screen_Selector
from node import Node

class Quantities_Screen(Screen):
	def __init__(self, quantities_data, screenmanager, **kwargs):
		super().__init__(**kwargs)
		self.name = 'Quantities_Screen'
		self.add_widget(Quantities_Layout(quantities_data, screenmanager))

class Quantities_Layout(RelativeLayout):
	def __init__(self, quantities_data, screenmanager, **kwargs):
		super().__init__(**kwargs)

		self.popups = []

		# setup the tree to view the database
		kwargs = {'size_hint': (1, 0.8), 'pos_hint': {'center_y': 0.5}}
		VD = View_Ingredient_Scaffold(quantities_data, **kwargs)
		self.add_widget(VD)

		popLayout = Add_Quantity_Layout(self, quantities_data, Add_Quantity_Button)
		myAddPop = Popup(title='Add Quantity', content=popLayout, size_hint=(0.75, 0.75))
		self.popups.append(myAddPop)

		kwargs = {'text': 'Add Quantity', 'size_hint': (0.5, 0.1), 'pos_hint': {'right': 1}}
		addButton = Launch_Popup(myAddPop, **kwargs)
		self.add_widget(addButton)

		# remove button
		# kwargs = {'text': 'Remove Quantity', 'size_hint': (0.5, 0.1), 'pos_hint': {'x': 0, 'y': 0}}
		# remButton = Remove_From_TreeView(VD, quantities_data, **kwargs)
		# self.add_widget(remButton)

		# remove button
		myRemovePop = Remove_Quantity_Layout(self, VD, quantities_data, Remove_From_TreeView_Popup)
		removePop =Popup(title='Remove Ingredient', content=myRemovePop, size_hint=(0.75, 0.75))
		self.popups.append(removePop)

		kwargs = {'text': 'Remove Ingredient', 'size_hint': (0.5, 0.1), 'pos_hint': {'x': 0, 'y': 0}}
		remButton =Launch_Popup(removePop, **kwargs)
		self.add_widget(remButton)

		# # add the button to switch to recipes
		kwargs = {'size_hint': (1, 0.1), 'pos_hint': {'top': 1}}
		selector = Screen_Selector(screenmanager, **kwargs)
		selector.quantities_screen_button.background_color = (0, 1, 0, 1)
		self.add_widget(selector)


class Add_Quantity_Layout(PopLayoutOkCancel):
	def __init__(self, screen_layout, observable_data, add_from_popup, **kwargs):
		buttonArgs = {}
		buttonArgs['observable_data'] = observable_data
		buttonArgs['screen_layout'] = screen_layout
		buttonArgs['pop_layout'] = self
		super().__init__(screen_layout, add_from_popup, buttonArgs, **kwargs)

		kwargs = {'text': 'Enter Value', 'size_hint': (1, 0.1), 'pos_hint': {'center_y': 0.9}}
		self.text_input = TextInput(**kwargs)
		self.add_widget(self.text_input)

	@property
	def data_dict(self):
		return {'name': self.text_input.text}

class Add_Quantity_Button(Add_Node_From_Popup):

	@property
	def my_node(self):
		return Node(name=self.pop_layout.data_dict['name'])

class Remove_Quantity_Layout(PopLayoutOkCancel):

	def __init__(self, screen_layout, tree_view, observer_database, remove_from_treeview_button, **kwargs):

		buttonArgs = {}
		buttonArgs['screen_layout'] = screen_layout
		buttonArgs['tree_view'] = tree_view
		buttonArgs['observer_database'] = observer_database

		super().__init__(screen_layout, remove_from_treeview_button, buttonArgs, **kwargs)

		kwargs = {'size_hint': (1, 0.9), 'pos_hint': {'top': 1}}
		myLabel = Label(text='Delete Quantity?', **kwargs)
		self.add_widget(myLabel)
