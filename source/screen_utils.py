from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class Screen_Button(Button):
	def __init__(self, screen_manager, screen_name, **kwargs):
		super().__init__(**kwargs)
		self.screen_manager = screen_manager
		self.screen_name = screen_name

	def on_press(self):
		self.screen_manager.current = self.screen_name


class Screen_Selector(BoxLayout):
	
	def __init__(self, screen_manager, **kwargs):
		super().__init__(**kwargs)
		orientation = 'horizontal'

		self.ingredient_screen_button =  Screen_Button(screen_manager, 'Ingredients_Screen', text='Ingredient Screen')

		self.quantities_screen_button =  Screen_Button(screen_manager, 'Quantities_Screen', text='Quantities Screen')

		self.recipe_screen_button =  Screen_Button(screen_manager, 'Cookbook_Home_Screen', text='Cookbook Screen')

		self.add_widget(self.ingredient_screen_button)
		self.add_widget(self.quantities_screen_button)
		self.add_widget(self.recipe_screen_button)
