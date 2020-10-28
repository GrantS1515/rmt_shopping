from kivy.uix.button import Button
from node import Node

class Remove_From_TreeView(Button):
	def __init__(self, tree_view, observer_database, **kwargs):
		super().__init__(**kwargs)
		self.observer_database = observer_database
		self.tree_view = tree_view
		self.__temp_node__ = Node(name='temp')

	def on_press(self):
		tree_node = self.tree_view.selected_node
		if tree_node != None:

			if tree_node.text != 'Root':
				ingredient = self.observer_database.get_node(self.__temp_node__.str2name(tree_node.text))
				self.observer_database.remove(ingredient)
				self.observer_database.save()
				self.observer_database.update_observers()