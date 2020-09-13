from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.clock import Clock
from kivy.uix.label import Label

class View_Database(TreeView):

	def __init__(self, data, **kwargs):
		super().__init__(**kwargs)
		self.data = data
		self.data.observers.append(self)
		self.update()

	def _clear_view(self):
		for tree_node in list(self.iterate_all_nodes()):
			self.remove_node(tree_node)

	def _build_view(self, dt):
		raise NotImplementedError
	
	def update(self):
		self._clear_view()
		Clock.schedule_once(self._build_view, 0.1)

class View_Ingredient_Scaffold(View_Database):
	def __init__(self, data, **kwargs):
		super().__init__(data, **kwargs)

	def _build_view(self, dt):
		for ingredient in self.data:
			TV_node = TreeViewLabel(text=ingredient.__str__())
			self.add_node(TV_node)

class View_Recipe_Node(Label):

	def __init__(self, recipe_node, **kwargs):
		super().__init__(**kwargs)
		self.recipe_node = recipe_node

	def update(self):
		self.text = self.recipe_node.__str__()