import pickle
import os

class Leaf():
	def __init__(self, name, **kwargs):
		self.name = name
		self.parents = set()
		self.children = set()

	def __eq__(self, other):
		if other == None:
			return False

		else:
			return (self.name == other.name) and (self.parents == other.parents) and (self.children == other.children)

class Tree():
	def __init__(self, leaf_class, **kwargs):
		self._LeafDict = {}
		self.leaf_class = leaf_class

	def get_leaf(self, leaf_name):

		if leaf_name not in self._LeafDict:
			raise Exception('Leaf not in tree')

		return self._LeafDict[leaf_name]

	def add(self, leaf_name, parents_names=None, **kwargs):

		# find or create the leaf
		if leaf_name in self._LeafDict:
			leaf = self._LeafDict[leaf_name]
		else:
			leaf = self.leaf_class(leaf_name, **kwargs)
			self._LeafDict[leaf.name] = leaf

		# assign the parent names
		if parents_names == None:
			parents_names = set()

		leaf.parents |= parents_names
			
		# assign the parents to new leaf as a child
		for parent_name in leaf.parents:
			self.get_leaf(parent_name).children |= {leaf.name}

	def remove(self, leaf_name):
		'''
		Remove a leaf and all the children of the leaf
		'''

		if leaf_name not in self._LeafDict:
			raise Exception('Leaf not in tree')

		leaf = self.get_leaf(leaf_name)

		for parent_leaf_name in leaf.parents:
			self.get_leaf(parent_leaf_name).children.remove(leaf_name)

		for child_leaf_name in leaf.children:
			self.get_leaf(child_leaf_name).parents.remove(leaf_name)

		leaf.parents = set()
		leaf.children = set()
		del self._LeafDict[leaf.name]

	def __iter__(self):
		return self._LeafDict.values().__iter__()

	def __eq__(self, other):
		return True

class Shopping_Tree(Tree):

	def __init__(self, leaf_class, filename, **kwargs):
		super().__init__(leaf_class, **kwargs)
		self.filename = filename + '.tree'

		if os.path.exists(self.filename):
			with open(self.filename, 'rb') as f:
				self._LeafDict = pickle.load(f)

	def save(self):
		with open(self.filename, 'wb') as f:
			pickle.dump(self._LeafDict, f)