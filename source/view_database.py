from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.clock import Clock

class View_Ingredient_Database(TreeView):

	def __init__(self, ingredient_data, **kwargs):
		super().__init__(**kwargs)
		self.ingredient_data = ingredient_data
		self.ingredient_data.observers.append(self)

	def _clear_view(self):
		for tree_node in list(self.iterate_all_nodes()):
			self.remove_node(tree_node)

	def _build_view(self, dt):
		raise NotImplementedError
	
	def update(self):
		self._clear_view()
		Clock.schedule_once(self._build_view, 0.1)


class View_Ingredient_Scaffold(View_Ingredient_Database):
	def __init__(self, ingredient_data, **kwargs):
		super().__init__(ingredient_data, **kwargs)

	def _build_view(self, dt):
		for ingredient in self.ingredient_data:
			TV_node = TreeViewLabel(text=ingredient.__str__())
			self.add_node(TV_node)