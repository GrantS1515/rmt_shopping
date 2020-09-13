from abc import ABC, abstractmethod
import os
import json
from node import Node, Quantity_Ingredient, Recipe_Node

class Observable_Database(ABC):

	@abstractmethod
	def __init__(self, filename, **kwargs):
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

	def update_observers(self):
		for observer in self.observers:
			observer.update()

class OD_Scaffold(Observable_Database):

	def __init__(self, filename, **kwargs):
		self.data = {}
		super().__init__(filename, **kwargs)

	def _load_file(self):
		if os.path.exists(self.filename):
			with open(self.filename, 'r') as f:
				data = json.load(f)

			for v in data.values():
				if v.get('is_node', False):
					self.add(Node(json_data=v))
				elif v.get('is_QI', False):
					self.add(Quantity_Ingredient(json_data=v))
				elif v.get('is_recipe', False):
					self.add(Recipe_Node(json_data=v))

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

	def __iter__(self):
		return self.data.values().__iter__()
