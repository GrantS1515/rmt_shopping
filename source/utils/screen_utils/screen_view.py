from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty

class Basic_Menu_View_Node(ToggleButton):

	def __init__(self, command_node, group_name, **kwargs):
		kwargs['text'] = command_node.name
		kwargs['group'] = group_name
		super().__init__(**kwargs)
		self.name = command_node.name
		self.command_node = command_node
		
class MyVerticalMenu(RelativeLayout):

	command_node = ObjectProperty()


	def __init__(self, menu_graph, size_hint_dropdown, right=True, **kwargs):
		'''
		args:
			kwargs must contain both size_hint and pos_hint with both x, y sizes and positions

		# TODO
		# add a scroll bar that would allow me to scroll down the butttons
		# set a min size for both the main buttons and the dropdown options
		'''

		my_args = {'size_hint': (1, 1)}
		super().__init__(**my_args)
		
		action_layout = BoxLayout(orientation='vertical', **kwargs)
		size_hint_x = self.__size_hint_x(kwargs)
		size_hint_y = self.__size_hint_y(kwargs)
		size_hint = (size_hint_x, size_hint_y) 
		x = self.__x_pos_hint(kwargs['pos_hint'], size_hint)
		y = self.__y_pos_hint(kwargs['pos_hint'], size_hint)
		size_hint_x_DD, size_hint_y_DD = size_hint_dropdown


		num_buttons = len(list(menu_graph.G.successors('Root')))
		self.main_btn_list = []
		self.btntxt2DD = {}
		self.dd_btn_list = []

		for i, main_graph_node in enumerate(menu_graph.G.successors('Root')):
			main_btn = menu_graph.G.node[main_graph_node]['view_node']
			action_layout.add_widget(main_btn)
			self.main_btn_list.append(main_btn)

			dd_x = self.__get_pos_x(x, size_hint_x, size_hint_x_DD, right)
			dd_y = self.__get_pos_y(i, num_buttons, size_hint_y, size_hint_y_DD)
			my_args = {'size_hint': (size_hint_x_DD, size_hint_y_DD),
			'pos_hint': {'x': dd_x, 'y': dd_y}}

			DD = MyDropDown(self, **my_args)
			self.btntxt2DD[main_btn.text] = DD
			main_btn.bind(on_press=self._update_main_menu)

			for dd_graph_node in menu_graph.G.successors(main_graph_node):
				dd_btn = menu_graph.G.node[dd_graph_node]['view_node']
				self.dd_btn_list.append(dd_btn)
				DD.add_widget(dd_btn)

		self.add_widget(action_layout)
		self.action_layout = action_layout
		self.active_DD = None

	def _update_main_menu(self, button=None):
		self.active_DD = None
		for btntxt, DD in self.btntxt2DD.items():
			if (button.text == btntxt) and (button.state == 'down'):
				DD.open(button)
				self.active_DD = DD
			else:
				DD.close(button)

		# clost down the dropdown buttons to give user chance to select
		for btn in self.dd_btn_list:
			btn.state = 'normal'

	def btn_select(self, view_node):
		
		if view_node.state == 'down':
			self.command_node = view_node.command_node

	def on_touch_down(self, touch):

		pass_on_touch = True

		if self.active_DD != None:

			if not self.active_DD.collide_point(*touch.pos):

				self.active_DD.close(None)
				self.active_DD = None
				for btn in self.main_btn_list:
					btn.state = 'normal'

			else:

				hit_btn = None
				for btn in self.dd_btn_list:
					if btn.collide_point(*touch.pos):
						btn.state = 'down'
						hit_btn = btn
					else:
						btn.state = 'normal'

				self.btn_select(hit_btn)

				return True


		super().on_touch_down(touch)

	@staticmethod
	def __x_pos_hint(pos_hint_dict, size_hint_tuple):
		if 'x' in pos_hint_dict:
			return pos_hint_dict['x']
		elif 'right' in pos_hint_dict:
			return pos_hint_dict['right'] - size_hint_tuple[0]
		elif 'center_x' in pos_hint_dict:
			return pos_hint_dict['center_x'] - size_hint_tuple[0] / 2
		elif 'center' in pos_hint_dict:
			return pos_hint_dict['center'][0] - size_hint_tuple[0] / 2
		else:
			raise Exception('Need to define x coordinate in pos_hint')

	@staticmethod
	def __y_pos_hint(pos_hint_dict, size_hint_tuple):
		if 'y' in pos_hint_dict:
			return pos_hint_dict['x']
		elif 'top' in pos_hint_dict:
			return pos_hint_dict['top'] - size_hint_tuple[1]
		elif 'center_y' in pos_hint_dict:
			return pos_hint_dict['center_y'] - size_hint_tuple[1] / 2
		elif 'center' in pos_hint_dict:
			return pos_hint_dict['center'][1] - size_hint_tuple[1] / 2
		else:
			raise Exception('Need to define x coordinate in pos_hint')

	@staticmethod
	def __size_hint_x(kwargs):
		if 'size_hint' in kwargs:
			return kwargs['size_hint'][0]
		elif 'size_hint_x' in kwargs:
			return kwargs['size_hint_x']
		else:
			raise Exception('Need to define x coordinate of size_hint')

	@staticmethod
	def __size_hint_y(kwargs):
		if 'size_hint' in kwargs:
			return kwargs['size_hint'][1]
		elif 'size_hint_y' in kwargs:
			return kwargs['size_hint_y']
		else:
			raise Exception('Need to define y coordinate of size_hint')

	@staticmethod
	def __get_pos_y(i_button, num_buttons, size_hint_y, size_hint_y_DD):
		return size_hint_y - (size_hint_y / num_buttons) * i_button - size_hint_y_DD
		# return (i_button + 1) * (size_hint_y / num_buttons) - size_hint_y_DD

	@staticmethod
	def __get_pos_x(x, size_hint_x, size_hint_x_DD, right=True):
		if right:
			return x + size_hint_x
		else:
			return x - size_hint_x_DD

class MyDropDown(BoxLayout):
	def __init__(self, parent_relative, **kwargs):
		super().__init__(**kwargs)
		self.orientation = 'vertical'
		self.parent_relative = parent_relative
		self.viewed = False

	def open(self, button):
		if self.viewed:
			return

		self.parent_relative.add_widget(self)
		self.viewed = True

	def close(self, button):
		if not self.viewed:
			return

		self.parent_relative.remove_widget(self)
		self.viewed = False
