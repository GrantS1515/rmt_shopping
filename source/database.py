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

	@abstractmethod
	def save(self):
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
		super().__init__(filename, **kwargs)
		self.filename = filename + 'data'
		self.data = {}

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