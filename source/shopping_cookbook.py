from kivy.uix.screenmanager import Screen
from kivy.uix.relativelayout import RelativeLayout

class Shopping_Cookbook_Screen(Screen):
	def __init__(self, screen_manager, **kwargs):
		super().__init__(**kwargs)
		self.name = 'Shopping_Cookbook_Screen'
		self.add_widget(Shopping_Cookbook_Layout(screen_manager))

class Shopping_Cookbook_Layout(RelativeLayout):
	def __init__(self, screen_manager, **kwargs):
		super().__init__(**kwargs)