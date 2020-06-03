from kivy.uix.screenmanager import Screen
from kivy.uix.relativelayout import RelativeLayout
from view_database import View_Ingredient_Scaffold
from kivy.uix.popup import Popup
from add_ingredient_popup import Add_Ingredient_Layout_Scaffold
from general_classes import Launch_Popup, Remove_From_TreeView, Screen_Selector

class Ingredients_Screen(Screen):
	def __init__(self, ingredient_data, screenmanager, **kwargs):
		super().__init__(**kwargs)
		self.name = 'Ingredients_Screen'
		self.add_widget(IngredientLayout(ingredient_data, screenmanager))

class IngredientLayout(RelativeLayout):
	def __init__(self, ingredient_data, screenmanager, **kwargs):
		super().__init__(**kwargs)

		# setup the tree to view the database
		kwargs = {'size_hint': (1, 0.8), 'pos_hint': {'center_y': 0.5}}
		VD = View_Ingredient_Scaffold(ingredient_data, **kwargs)
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
		remButton = Remove_From_TreeView(VD, ingredient_data, **kwargs)
		self.add_widget(remButton)

		# add the button to switch to recipes
		kwargs = {'size_hint': (1, 0.1), 'pos_hint': {'top': 1}}
		selector = Screen_Selector(screenmanager, **kwargs)
		selector.ingredient_screen_button.background_color = (0, 1, 0, 1)
		self.add_widget(selector)



