import pickle
import os

class Leaf():

	'''
	A leaf contains a name, parents and children
	'''

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

	''' Create a Tree data structure with leafs that allow multiple parents
	'''

	def __init__(self, leaf_class, **kwargs):
		self._LeafDict = {}
		self.leaf_class = leaf_class

	@property
	def _root_leaf_names(self):
		'''
		Return a set of leaf names connected to the root leaf
		'''
		root_set = set()
		for leaf_name in self.__iter__():
			if self.get_leaf(leaf_name).parents == set():
				root_set.add(leaf_name)

		return root_set

	def get_leaf(self, leaf_name):
		'''
		Return a leaf given a name of it as long as it exists. A leaf_name that does not exist causes an exception to be raised.

		Args:
			leaf_name: str name of the leaf

		Raises:
			Exception: with text 'Leaf not in tree'

		Returns:
			Leaf that corresponds to leaf_name
		'''

		if leaf_name not in self._LeafDict:
			raise Exception('Leaf not in tree')

		return self._LeafDict[leaf_name]

	def add(self, leaf_name, parents_names=None, **kwargs):

		'''
		Add a Leaf to the tree. If a leaf already exists by that name then it appends the parents to the already existing leaf.

		Args:
			leaf_name: str of the name the leaf is called

			parents_names: set of names that you want the leaf to be connected to
		'''

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
		Remove a leaf and all the children of the leaf.

		Args:
			leaf_name: str name of the leaf to be removed
		'''

		contacted_leaf_names = set()
		deleted_leaf_names = set()
		parent_leafs = self.get_leaf(leaf_name).parents
		
		self._remove_leaf_set({leaf_name}, contacted_leaf_names, deleted_leaf_names)

		# parent leafs represent all the leafs that have not been deleted, but still have pointers to leafs that have been deleted... so those pointers must be deleted
		parent_leafs |= (contacted_leaf_names - deleted_leaf_names)
		for name in parent_leafs:

			for deleted_name in deleted_leaf_names:

				leaf = self.get_leaf(name) 
				leaf.children -= {deleted_name}
				leaf.parents -= {deleted_name}

	def _remove_leaf_set(self, leaf_name_set, contacted_leaf_names, deleted_leaf_names):

		for leaf_name in leaf_name_set:

			contacted_leaf_names.add(leaf_name)

			leaf = self.get_leaf(leaf_name)

			# recursive set of going to the children and deleting them
			if leaf.children != set():
				self._remove_leaf_set(leaf.children, contacted_leaf_names, deleted_leaf_names)
			
			# save the leaf when another parent is there but otherwise delete that leaf
			if len(leaf.parents) <= 1:
				deleted_leaf_names.add(leaf.name)
				leaf.parent = set()
				del self._LeafDict[leaf.name]

	def bfs(self):
		'''
		Return a generator that implments breadth first search returning the names of the leafs
		'''

		q = list(self._root_leaf_names)

		while q != []:
			myVal = q.pop(0)

			if myVal != set():
				q.extend(self.get_leaf(myVal).children)

			yield myVal

	def __iter__(self):
		return self._LeafDict.keys().__iter__()

	def __eq__(self, other):
		
		if len(self._LeafDict) != len(other._LeafDict):
			return False

		for leaf_name in self._LeafDict.keys():
			if self.get_leaf(leaf_name) != other.get_leaf(leaf_name):
				return False

		return True

class Shopping_Tree(Tree):

	'''
	Implement an extension of Tree that includes an interface suitable for the shopping app.
	'''

	def __init__(self, leaf_class, filename, **kwargs):
		'''
		Create a shopping tree. Build using leafs of type leaf_class. If a filename exists then that tree is loaded. Else, a new file is made

		Args:
			leaf_class: Reference to the type of Leaf to use in the Shopping_Tree

			filename: path to where to save and load the tree
		'''
		super().__init__(leaf_class, **kwargs)
		self.filename = filename + '.tree'
		self.observers = [] #: list: of observer objects -- which must have an update() method

		if os.path.exists(self.filename):
			with open(self.filename, 'rb') as f:
				self._LeafDict = pickle.load(f)

			# add exception to ensure leaf_class matches the read file

	def save(self):
		'''
		Save the tree to the initialized filename.
		'''
		with open(self.filename, 'wb') as f:
			pickle.dump(self._LeafDict, f)

	def update(self):
		'''
		For each observer call their update()
		'''

		for observer in self.observers:
			observer.update(self)

