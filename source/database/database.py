from abc import ABC, abstractmethod, abstractproperty
import os
import json
import database.node as nd
import networkx as nx
import networkx.readwrite.json_graph as json_graph

###TODO
# Modify update so that it looks at the file again and reloads file data again

class Observable_Database(ABC):

	@abstractmethod
	def __init__(self, filename, **kwargs):
		'''Make an observable database of nodes
		'''
		self.observers = []
		self.filename = filename
		self._load_file()
		self.coreid2core_func = {}
		self.coreid2self_func = {}

	@abstractmethod
	def save(self):
		pass

	@abstractmethod
	def _load_file(self):
		pass

	@abstractmethod
	def add(self, node, **kwargs):
		pass

	@abstractmethod
	def remove(self, node, **kwargs):
		pass

	@abstractmethod
	def get_node(self, node_name):
		pass

	@abstractmethod
	def __iter__(self):
		pass

	def attach_core(self, core, process_core=None, process_self=None):
		core.observers.append(self)
		self.coreid2core_func[id(core)] = process_core
		self.coreid2self_func[id(core)] = process_self

	def update_observers(self):
		for observer in self.observers:
			observer.update(self)

	def update(self, core):
		'''Called when core updates this database
		'''
		pass

	@abstractmethod
	def predecessors(self, node):
		pass

	@abstractmethod
	def successors(self, node):
		pass

class OD_Scaffold(Observable_Database):

	def __init__(self, filename, **kwargs):
		self.data = {}
		super().__init__(filename, **kwargs)

	def _load_file(self):
		if os.path.exists(self.filename + '_node_data.json'):
			with open(self.filename + '_node_data.json', 'r') as f:
				data = json.load(f)

			for v in data.values():
				curr_node = None

				if v.get('is_node', False):
					curr_node = nd.Node(json_data=v)
				elif v.get('is_QI', False):
					curr_node = nd.Quantity_Ingredient(json_data=v)
				elif v.get('is_recipe', False):
					curr_node = nd.Recipe_Node(json_data=v)


				if curr_node != None:
					self.add(curr_node)
					
	def save(self):

		json_data = {}
		for k, v in self.data.items():
			json_data[k] = v.json_encoder()

		with open(self.filename + '_node_data.json', 'w') as f:
			json.dump(json_data, f)
	
	def add(self, node, **kwargs):
		self.data[node.name] = node

	def remove(self, node, **kwargs):
		del self.data[node.name]

	def get_node(self, node_name):
		return self.data[node_name]

	def update(self, core):
		'''Update this database with another database
		'''
		process_core = self.coreid2core_func[id(core)]
		core_name_set = process_core(core)
		process_self = self.coreid2self_func[id(core)]

		for node in tuple(self.data.values()):

			if not process_self(node).issubset(core_name_set):
				self.remove(node)

		self.update_observers()
		self.save()		

	def __iter__(self):
		return self.data.values().__iter__()

	def predecessors(self, node):
		return []

	def successors(self, node):
		return []

class OD_DAG(Observable_Database):
	def __init__(self, filename, **kwargs):
		self.graph = nx.DiGraph()
		self.graph.add_node('Root')
		self.data = {}
		super().__init__(filename, **kwargs)

	def _load_file(self):
		if os.path.exists(self.filename + '_graph.json'):
			with open(self.filename + '_graph.json', 'r') as f:
				graph_json = json.load(f)
				self.graph = json_graph.node_link_graph(graph_json)


		if os.path.exists(self.filename + '_node_data.json'):
			with open(self.filename + '_node_data.json', 'r') as f:
				data = json.load(f)

			for v in data.values():
				curr_node = None

				if v.get('is_node', False):
					curr_node = nd.Node(json_data=v)
				elif v.get('is_QI', False):
					curr_node = nd.Quantity_Ingredient(json_data=v)
				elif v.get('is_recipe', False):
					curr_node = nd.Recipe_Node(json_data=v)

				if curr_node != None:
					self.data[curr_node.name] = curr_node

	def save(self):
		graph_data = json_graph.node_link_data(self.graph)
		with open(self.filename + '_graph.json', 'w') as f:
			json.dump(graph_data, f)

		json_data = {}
		for k, v in self.data.items():
			json_data[k] = v.json_encoder()

		with open(self.filename + '_node_data.json', 'w') as f:
			json.dump(json_data, f)

	def add(self, node, parent_node=None, **kwargs):

		if node.name not in self.graph:
			self.graph.add_node(node.name)
			self.data[node.name] = node

		if parent_node != None:
			if (parent_node.name not in self.graph):
				self.graph.add_node(parent_node.name)
				self.data[parent_node.name] = parent_node
			self.graph.add_edge(parent_node.name, node.name)

			if not nx.is_directed_acyclic_graph(self.graph):
				self.graph.remove_edge(parent_node.name, node.name)
				raise ValueError

		else: 
			self.graph.add_edge('Root', node.name)


	def remove(self, node):

		if list(self.graph.predecessors(node.name)) == ['Root']:
			for s_node_name in tuple(self.graph.successors(node.name)):
				self.graph.add_edge('Root', s_node_name)

		self.graph.remove_node(node.name)
		del self.data[node.name]

	def get_node(self, node_name):
		return self.data[node_name]

	def update(self, core):
		process_core = self.coreid2core_func[id(core)]
		core_name_set = process_core(core)
		process_self = self.coreid2self_func[id(core)]

		for node_name in tuple(self.data):

			if not {node_name}.issubset(core_name_set):
				self.remove(self.get_node(node_name))

		self.update_observers()
		self.save()

	def __iter__(self):
		node_names = nx.bfs_tree(self.graph, 'Root')
		myNodes = [self.get_node(node_name) for node_name in node_names if node_name != 'Root']
		return iter(myNodes)

	def predecessors(self, node):
		return [self.get_node(i) for i in tuple(self.graph.predecessors(node.name)) if i != 'Root']

	def successors(self, node):
		return [self.get_node(i) for i in tuple(self.graph.successors(node.name)) if i != 'Root']