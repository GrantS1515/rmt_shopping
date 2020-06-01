import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout

from database import OD_Scaffold
from view_database import View_Ingredient_Scaffold


# temp
from kivy.uix.treeview import TreeView

class Temp(RelativeLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		ingredient_data = OD_Scaffold('temp')
		VI = View_Ingredient_Scaffold(ingredient_data)
		ingredient_data.update_observers()

		self.add_widget(VI)
		

class TempApp(App):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def build(self):
		return Temp()

if __name__ == '__main__':
	TempApp().run()