from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout

class View_Database(RelativeLayout):
	
	def __init__(self, data, **kwargs):
		self.data = data
		self.data.observers.append(self)
		super().__init__(size_hint=(1, 1))

	@property
	def my_selected_node(self):
		raise NotImplementedError

	def update(self):
		raise NotImplementedError

class Viewable_TreeView(TreeView):
	def __init__(self, data, **kwargs):
		super().__init__(**kwargs)
		self._nodestr2node = {}
		self.data = data
		self._build_view(0)
		
	def _clear_view(self):
		for tree_node in list(self.iterate_all_nodes()):
			self.remove_node(tree_node)

	def _build_view(self, dt):
		for node in self.data:
			node_str = node.__str__()
			self._nodestr2node[node_str] = node
			TV_node = TreeViewLabel(text=node_str)
			self.add_node(TV_node)

	@property
	def my_selected_node(self):
		tree_node = self.selected_node

		if tree_node == None:
			return None
		elif tree_node.text == 'Root':
			return None
		else:
			return self._nodestr2node[tree_node.text]

	def update(self):
		self._clear_view()
		Clock.schedule_once(self._build_view, 0.1)

class View_Nodes_Scaffold(View_Database):
	def __init__(self, data, **kwargs):
		super().__init__(data, **kwargs)
		self.TV = Viewable_TreeView(data, **kwargs)
		self.add_widget(self.TV)
		self.update()

	@property
	def my_selected_node(self):
		return self.TV.my_selected_node

	def update(self):
		self.TV.update()

class View_Nodes_Scroll(View_Database):
	def __init__(self, data, **kwargs):
		super().__init__(data, **kwargs)
		kwargs['bar_inactive_color'] = [0.7, 0.7, 0.7, 1]
		kwargs['bar_margin'] = 5
		kwargs['bar_width'] = 10
		SV = ScrollView(**kwargs)
		

		kwargs = {'size_hint': (kwargs['size_hint'][0], None)}
		self.TV = Viewable_TreeView(data, **kwargs)
		self.TV.bind(minimum_height = self.TV.setter('height'))
		SV.add_widget(self.TV)

		self.add_widget(SV)

	def update(self):
		self.TV.update()

	@property
	def my_selected_node(self):
		return self.TV.my_selected_node


class View_Recipe_Node(Label):

	def __init__(self, recipe_node, **kwargs):
		super().__init__(**kwargs)
		self.recipe_node = recipe_node
		self.recipe_node.observers.append(self)

	def update(self):
		self.text = self.recipe_node.__str__()