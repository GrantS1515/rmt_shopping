from kivy.uix.screenmanager import Screen
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

import database.view as view
import database.node as nd
import utils.popup_utils as pu
import utils.screen_utils as su


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
		VD = view.View_Nodes_Scroll(quantities_data, **kwargs)
		self.add_widget(VD)

		popLayout = Add_Quantity_Layout(self, quantities_data, Add_Quantity_Button)
		myAddPop = Popup(title='Add Quantity', content=popLayout, size_hint=(0.75, 0.75))
		self.popups.append(myAddPop)

		kwargs = {'text': 'Add Quantity', 'size_hint': (0.5, 0.1), 'pos_hint': {'right': 1}}
		addButton = pu.Launch_Popup(myAddPop, **kwargs)
		self.add_widget(addButton)

		# remove button
		myRemovePop = Remove_Quantity_Layout(self, VD, quantities_data, pu.Remove_From_Database_Button)
		removePop =Popup(title='Remove Ingredient', content=myRemovePop, size_hint=(0.75, 0.75))
		self.popups.append(removePop)

		kwargs = {'text': 'Remove Ingredient', 'size_hint': (0.5, 0.1), 'pos_hint': {'x': 0, 'y': 0}}
		remButton =pu.Launch_Popup(removePop, **kwargs)
		self.add_widget(remButton)

		# add the button to switch to recipes
		kwargs = {'size_hint': (1, 0.1), 'pos_hint': {'top': 1}}
		selector = su.Screen_Selector(screenmanager, **kwargs)
		selector.quantities_screen_button.background_color = (0, 1, 0, 1)
		self.add_widget(selector)


class Add_Quantity_Layout(pu.PopLayoutOkCancel):
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

class Add_Quantity_Button(pu.Add_Node_From_Popup):

	@property
	def my_node(self):
		return nd.Node(name=self.pop_layout.data_dict['name'])

class Remove_Quantity_Layout(pu.PopLayoutOkCancel):

	def __init__(self, screen_layout, view_database, observer_database, remove_from_database_button, **kwargs):

		buttonArgs = {}
		buttonArgs['screen_layout'] = screen_layout
		buttonArgs['view_database'] = view_database
		buttonArgs['observer_database'] = observer_database

		super().__init__(screen_layout, remove_from_database_button, buttonArgs, **kwargs)

		kwargs = {'size_hint': (1, 0.9), 'pos_hint': {'top': 1}}
		myLabel = Label(text='Delete Quantity?', **kwargs)
		self.add_widget(myLabel)
