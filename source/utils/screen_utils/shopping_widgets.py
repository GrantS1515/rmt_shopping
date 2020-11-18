import os

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout

import utils.screen_utils.screen_control as sc
import utils.screen_utils.screen_model as sm
import utils.screen_utils.screen_view as sv
import database.view_manager as vm

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

class Action_Bar(RelativeLayout):
	
	def __init__(self, view_path, add_data_command_node):
		super().__init__()

		kwargs = {'pos_hint': {'top': 1, 'right': 1}, 'size_hint': (0.9, 1)}
		VM = vm.View_Manager(view_path, **kwargs)
		self.currView = VM.view_scaffold
		self.add_widget(self.currView)

		C_classify = sc.Command_Node('Categorize')
		V_classify = sv.Basic_Menu_View_Node(C_classify, 'main')

		C_list = sc.Switch_View_Node('List', self, VM.view_scaffold)
		V_list = sv.Basic_Menu_View_Node(C_list, 'classify')

		MG = sm.Menu_Graph()
		MG.add_edge(V_classify)
		MG.add_edge(V_classify, V_list)

		for file in os.listdir():

			if file.endswith('_graph.json'):
				filename = str(file).split('_graph.json')[0]
				C_DD = sc.Switch_View_Node(filename, self, VM.filename2dag_view[filename])
				V_DD = sv.Basic_Menu_View_Node(C_DD, 'classify')
				MG.add_edge(V_classify, V_DD)

		C_add = sc.Command_Node('+')
		V_add = sv.Basic_Menu_View_Node(C_add, 'main')

		# C_data = sc.Switch_Screen_Node('Add Data Node', screen_manager, 'New_Data_Node_Screen')
		C_data = add_data_command_node
		V_data = sv.Basic_Menu_View_Node(C_data, '+data')

		MG.add_edge(V_add)
		MG.add_edge(V_add, V_data)

		menu_kwargs = {'size_hint': (0.1, 0.9), 'pos_hint': {'y': 0, 'x': 0}}
		SM = sv.MyVerticalMenu(MG, (0.25, 0.25), **menu_kwargs)
		self.add_widget(SM)
		SM.bind(command_node=self.btn_select)
		self.SM = SM

	def btn_select(self, object, value):
		value.execute()
		self.remove_widget(self.SM)
		self.add_widget(self.SM)

