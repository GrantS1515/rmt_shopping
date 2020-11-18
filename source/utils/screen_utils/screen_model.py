import networkx as nx

class Menu_Graph():

	def __init__(self):
		self.G = nx.DiGraph()
		self.G.add_node('Root')

	def add_edge(self, parent_node, child_node=None):

		parent_name = parent_node.name
		if parent_name not in self.G:
			self.G.add_node(parent_name, view_node=parent_node)
			self.G.add_edge('Root', parent_name)


		if child_node != None:
			
			if child_node.name not in self.G: 
				self.G.add_node(child_node.name, view_node=child_node)

			self.G.add_edge(parent_node.name, child_node.name)


		if not nx.is_directed_acyclic_graph(self.G):
			raise Exception('Edge Makes Menu Graph a non-DAG')