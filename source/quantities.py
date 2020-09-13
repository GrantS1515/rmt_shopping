from kivy.uix.screenmanager import Screen
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.popup import Popup

from view import View_Ingredient_Scaffold
from popup_utils import Launch_Popup, Add_Ingredient_Layout_Scaffold
from treeview_utils import Remove_From_TreeView
from screen_utils import Screen_Selector

class Quantities_Screen(Screen):
	def __init__(self, quantities_data, screenmanager, **kwargs):
		super().__init__(**kwargs)
		self.name = 'Quantities_Screen'
		self.add_widget(Quantities_Layout(quantities_data, screenmanager))

class Quantities_Layout(RelativeLayout):
	def __init__(self, quantities_data, screenmanager, **kwargs):
		super().__init__(**kwargs)

		# setup the tree to view the database
		kwargs = {'size_hint': (1, 0.8), 'pos_hint': {'center_y': 0.5}}
		VD = View_Ingredient_Scaffold(quantities_data, **kwargs)
		self.add_widget(VD)

		# make the popup
		pop_layout = Add_Ingredient_Layout_Scaffold()
		add_pop = Popup(title='Add Quantity', content=pop_layout, size_hint=(0.75, 0.75))
		pop_layout.load_layout(VD, quantities_data, add_pop)

		# # trigger the popup
		kwargs = {'text': 'Add Quantity', 'size_hint': (0.5, 0.1), 'pos_hint': {'right': 1}}
		addButton = Launch_Popup(add_pop, **kwargs)
		self.add_widget(addButton)

		# remove button
		kwargs = {'text': 'Remove Quantity', 'size_hint': (0.5, 0.1), 'pos_hint': {'x': 0, 'y': 0}}
		remButton = Remove_From_TreeView(VD, quantities_data, **kwargs)
		self.add_widget(remButton)

		# # add the button to switch to recipes
		kwargs = {'size_hint': (1, 0.1), 'pos_hint': {'top': 1}}
		selector = Screen_Selector(screenmanager, **kwargs)
		selector.quantities_screen_button.background_color = (0, 1, 0, 1)
		self.add_widget(selector)



