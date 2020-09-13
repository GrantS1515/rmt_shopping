import kivy
kivy.require('1.9.0')



from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from data.database import OD_Scaffold
from data.view_database import View_Ingredient_Scaffold
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from ingredient.add_ingredient_popup import Add_Ingredient_Layout_Scaffold

# temp


class Temp(RelativeLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		ingredient_data = OD_Scaffold('temp')

		kwargs = {'size_hint': (1, 0.5), 'pos_hint': {'top': 1}}
		VI = View_Ingredient_Scaffold(ingredient_data, **kwargs)
		ingredient_data.update_observers()
		self.add_widget(VI)

		# define popup

		layout = Add_Ingredient_Layout_Scaffold()
		popup = Popup(title='test', content=layout, size_hint=(0.75, 0.75))
		layout.load_layout(VI, ingredient_data, popup)


		# add the popup button
		b = myButton(popup, text='popup', size_hint=(1, 0.1), pos_hint={'y': 0})
		self.add_widget(b)


class myButton(Button):

	def __init__(self, popup, **kwargs):
		super().__init__(**kwargs)
		self.popup = popup

	def on_press(self):
		self.popup.open()


		

class TempApp(App):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def build(self):
		return Temp()

if __name__ == '__main__':
	TempApp().run()