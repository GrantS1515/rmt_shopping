from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.clock import Clock

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

class View_Recipe_Scaffold(View_Database):
	# def __init__(self, recipe_data, **kwargs):
	# 	super().__init__(recipe_data, **kwargs)

	def _build_view(self, dt):

		self._build_recipe(self.data)

		
	def _build_recipe(self, recipe):

		recipe_node = TreeViewLabel(text=recipe.name)
		self.add_node(recipe_node)

		for ing_quant in recipe:
			TV_node = TreeViewLabel(text=ing_quant.__str__())
			self.add_node(TV_node, recipe_node)

class View_Cookbook_Scaffold(View_Recipe_Scaffold):

	def _build_view(self, dt):
		for recipe in self.data:
			self._build_recipe(recipe)