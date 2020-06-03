from abc import ABC, abstractmethod
import pickle
import os

class Node():

	def __init__(self, name, **kwargs):
		self.name = name

	def __str__(self):
		return self.name

class Observable_Database(ABC):

	@abstractmethod
	def __init__(self, filename, **kwargs):
		self.observers = []
		self.filename = filename + '.data'
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
			with open(self.filename, 'rb') as f:
				self.data = pickle.load(f)


	def save(self):
		with open(self.filename, 'wb') as f:
			pickle.dump(self.data, f)

	def add(self, node, **kwargs):
		self.data[node.name] = node

	def remove(self, node, **kwargs):
		del self.data[node.name]

	def get_node(self, node_name):
		return self.data[node_name]

	def __iter__(self):
		return self.data.values().__iter__()

class Quantity_Ingredient(Node):

	def __init__(self, quantity, quantity_type, name, **kwargs):
		super().__init__(name, **kwargs)
		self.quantity = quantity
		self.quantity_type = quantity_type

	def __str__(self):
		return str(self.quantity) + ', ' + self.quantity_type + ' of ' + self.name

class Recipe_Scaffold(OD_Scaffold):
	def __init__(self, filename, name = None, **kwargs):
		self.name = name
		super().__init__(filename, **kwargs)
		
	def _load_file(self):
		if os.path.exists(self.filename):

			if self.name != None:
				raise Exception('Must not rename recipe when loading from file')

			with open(self.filename, 'rb') as f:
					self.data, self.name = pickle.load(f)

		if self.name == None:
			raise Exception('Must name recipe database')

	def save(self):
		data = (self.data, self.name)
		with open(self.filename, 'wb') as f:
			pickle.dump(data, f)