from abc import ABC, abstractmethod, abstractproperty
import os
import json
from node import Node, Quantity_Ingredient, Recipe_Node

class Observable_Database(ABC):

	@abstractmethod
	def __init__(self, filename, **kwargs):
		'''Make an observable database of nodes
		'''
		self.observers = []
		self.filename = filename
		self._load_file()

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

	@abstractmethod
	def collide(self, other_database, update_key):
		pass

	def update_observers(self):
		for observer in self.observers:
			observer.update()

	@abstractproperty
	def data_name_set(self):
		pass

	@abstractmethod
	def attach_core(self, core_database, update_key):
		'''Update this database with changes from core_database.

		args:
			core_database: type observable database
			update_key: str that indexes the node's node_name_dict
		'''

class OD_Scaffold(Observable_Database):

	def __init__(self, filename, **kwargs):
		'''
		args:
			core_databases: list of databases from which to update the data stored in this list
		'''

		self.data = {}
		self.core_databases = {}

		super().__init__(filename, **kwargs)

	def _load_file(self):
		if os.path.exists(self.filename):
			with open(self.filename, 'r') as f:
				data = json.load(f)

			for v in data.values():
				curr_node = None

				if v.get('is_node', False):
					curr_node = Node(json_data=v)
				elif v.get('is_QI', False):
					curr_node = Quantity_Ingredient(json_data=v)
				elif v.get('is_recipe', False):
					curr_node = Recipe_Node(json_data=v)


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

	def update(self):
		'''Given the list of core databases update this databases data
		'''
		for OD, is_consistent_func in self.core_databases.values():
			self.collide(OD, is_consistent_func)

		self.update_observers()
		self.save()

	def attach_core(self, core_database, is_consistent_func):
		self.core_databases[core_database.filename] = (core_database, is_consistent_func)
		core_database.observers.append(self)

	def collide(self, other_database, is_consistent_func):
		'''Return the names of nodes with a name set in this database but not the other_database
		'''
		for node in tuple(self.data.values()):

			if not is_consistent_func(other_database, node):
				self.remove(node)

	@property
	def data_name_set(self):
		name_set = set()
		for node in self.data.values():

			for node_name_set in node.node_name_dict.values():
				name_set |= node_name_set

		return name_set

	def __iter__(self):
		return self.data.values().__iter__()

def is_consistent_nodeOD_node(database, node):

	OD_name_set = set()
	OD_name_set |= set([i.name for i in database])

	return {node.name}.issubset(OD_name_set)

def is_consistent_ingredient_OD_recipe_node(ingredient_database, recipe_node):

	OD_name_set = set()
	OD_name_set |= set([i.name for i in ingredient_database])
	recipe_node_ingredients = set([i.name for i in recipe_node.QI_list])

	return recipe_node_ingredients.issubset(OD_name_set)

def is_consistent_quantity_type_OD_recipe_node(quantity_type_database, recipe_node):

	OD_name_set = set()
	OD_name_set |= set([i.name for i in quantity_type_database])
	recipe_node_ingredients = set([i.quantity_type for i in recipe_node.QI_list])

	return recipe_node_ingredients.issubset(OD_name_set)