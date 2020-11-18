import kivy
kivy.require('1.9.0')

import sys, os
sys.path.insert(0, os.path.abspath('..'))

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import FallOutTransition
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton

import networkx as nx

import database.database as db
import database.node as nd

import database.view_manager as vm
import utils.screen_utils.screen_control as sc
import utils.screen_utils.screen_model as sm
import utils.screen_utils.screen_view as sv
import utils.screen_utils.shopping_widgets as sw


class Test_New_Data_Node(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.name = 'New_Data_Node_Screen'

class Test_Screen(Screen):

	def __init__(self, path, screen_manager, **kwargs):
		super().__init__(**kwargs)

		C_data = sc.Switch_Screen_Node('Add Data Node', screen_manager, 'New_Data_Node_Screen')

		AB = sw.Action_Bar(path, C_data)
		self.add_widget(AB)

	# 	kwargs = {'pos_hint': {'top': 1, 'right': 1}, 'size_hint': (0.9, 1)}
	# 	VM = vm.View_Manager(path, **kwargs)
	# 	self.currView = VM.view_scaffold
	# 	self.add_widget(self.currView)

	# 	C_classify = sc.Command_Node('Categorize')
	# 	V_classify = sv.Basic_Menu_View_Node(C_classify, 'main')

	# 	C_list = sc.Switch_View_Node('List', self, VM.view_scaffold)
	# 	V_list = sv.Basic_Menu_View_Node(C_list, 'classify')

	# 	MG = sm.Menu_Graph()
	# 	MG.add_edge(V_classify)
	# 	MG.add_edge(V_classify, V_list)

	# 	for file in os.listdir():

	# 		if file.endswith('_graph.json'):
	# 			filename = str(file).split('_graph.json')[0]
	# 			C_DD = sc.Switch_View_Node(filename, self, VM.filename2dag_view[filename])
	# 			V_DD = sv.Basic_Menu_View_Node(C_DD, 'classify')
	# 			MG.add_edge(V_classify, V_DD)

	# 	C_add = sc.Command_Node('+')
	# 	V_add = sv.Basic_Menu_View_Node(C_add, 'main')
	# 	C_data = sc.Switch_Screen_Node('Add Data Node', screen_manager, 'New_Data_Node_Screen')
	# 	V_data = sv.Basic_Menu_View_Node(C_data, '+data')
	# 	MG.add_edge(V_add)
	# 	MG.add_edge(V_add, V_data)

	# 	menu_kwargs = {'size_hint': (0.1, 0.9), 'pos_hint': {'y': 0, 'x': 0}}
	# 	SM = sv.MyVerticalMenu(MG, (0.25, 0.25), **menu_kwargs)
	# 	self.add_widget(SM)
	# 	SM.bind(command_node=self.btn_select)
	# 	self.SM = SM

	# def btn_select(self, object, value):
	# 	value.execute()
	# 	self.remove_widget(self.SM)
	# 	self.add_widget(self.SM)
		

class Test(ScreenManager):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.transition = FallOutTransition()
		my_db = db.OD_DAG('ingredients')
		beans = nd.Node('Beans')
		black_beans = nd.Node('Black Beans')
		red_beans = nd.Node('Red Beans')
		my_db.add(beans)
		my_db.add(black_beans, beans)
		my_db.add(red_beans, beans)
		my_db.save()

		path = None
		
		self.add_widget(Test_Screen(path, self))
		self.add_widget(Test_New_Data_Node())

class TestApp(App):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def build(self):
		return Test()

if __name__ == '__main__':
	TestApp().run()