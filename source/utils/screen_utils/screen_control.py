from kivy.uix.button import Button


class Screen_Button(Button):
	def __init__(self, screen_manager, screen_name, **kwargs):
		super().__init__(**kwargs)
		self.screen_manager = screen_manager
		self.screen_name = screen_name

	def on_press(self):
		self.screen_manager.current = self.screen_name

class Command_Node():

	def __init__(self, name, **kwargs):
		self.name = name

	def excecute(self):
		pass

class Switch_Screen_Node(Command_Node):

	def __init__(self, name, screen_manager, screen_name, **kwargs):
		super().__init__(name, **kwargs)
		self.screen_manager = screen_manager
		self.screen_name = screen_name

	def execute(self):
		self.screen_manager.current = self.screen_name

class Switch_View_Node(Command_Node):

	def __init__(self, name, parent_screen, view, **kwargs):
		super().__init__(name, **kwargs)
		self.parent_screen = parent_screen
		self.view = view

	def execute(self):
		self.parent_screen.remove_widget(self.parent_screen.currView)
		self.parent_screen.currView = self.view
		self.parent_screen.add_widget(self.parent_screen.currView)