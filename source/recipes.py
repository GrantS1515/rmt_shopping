from kivy.uix.screenmanager import Screen
from general_classes import Screen_Selector, Screen_Button
from kivy.uix.relativelayout import RelativeLayout
from view_database import View_Cookbook_Scaffold

class Recipe_Screen(Screen):
	def __init__(self, recipes_data, screenmanager, **kwargs):
		super().__init__(**kwargs)
		self.name = 'Recipe_Screen'
		self.add_widget(Recipe_Layout(recipes_data, screenmanager))

class Recipe_Layout(RelativeLayout):
	def __init__(self, recipes_data, screenmanager, **kwargs):
		super().__init__(**kwargs)

		# add the view for recipes
		kwargs = {'size_hint': (1, 0.8), 'pos_hint': {'center_y': 0.5}}
		cookbook = View_Cookbook_Scaffold(recipes_data, **kwargs)
		cookbook.update()
		self.add_widget(cookbook)

		# add the buttons to add a new recipe
		kwargs = {'text': 'Add Recipe', 'size_hint': (0.3, 0.1), 'pos_hint': {'right': 1, 'y': 0}}
		SB = Screen_Button(screenmanager, 'Add_Recipe_Screen', **kwargs)
		self.add_widget(SB)

		# add a button to remove recipe

		# add the button to switch screens
		kwargs = {'size_hint': (1, 0.1), 'pos_hint': {'top': 1}}
		selector = Screen_Selector(screenmanager, **kwargs)
		selector.recipe_screen_button.background_color = (0, 1, 0, 1)
		self.add_widget(selector)