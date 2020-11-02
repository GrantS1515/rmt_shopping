from abc import ABC, abstractmethod, abstractproperty
import os
import json
import database.node as nd

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




class OD_Scaffold(Observable_Database):

	def __init__(self, filename, **kwargs):
		'''
		args:
			process_core_func: a static function taking database, node and returns bool if node is consistent with databases
		'''
		self.data = {}

		super().__init__(filename, **kwargs)

	def _load_file(self):
		if os.path.exists(self.filename):
			with open(self.filename, 'r') as f:
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

		with open(self.filename, 'w') as f:
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