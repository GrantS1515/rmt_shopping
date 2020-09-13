import pytest
from data.database import Node, OD_Scaffold, Recipe_Scaffold, Quantity_Ingredient
import os

class Observer_1():

	name = 'not assigned in observer_1'

	def update(self):
		self.name = 'observer_1'

class Observer_2():

	name = 'not assigned in observer_2'

	def update(self):
		self.name = 'observer_2'


@pytest.fixture
def tree_1():

	OD = OD_Scaffold('temp')

	fruit_node = Node('fruit')
	dessert_node = Node('dessert')
	meat_node = Node('meat')


	OD.add(fruit_node)
	OD.add(dessert_node)
	OD.add(meat_node)

	return OD

class Test_OD_interface_1():

	filename = 'temp'
	OD = OD_Scaffold('temp')
	OD_type = OD_Scaffold

	def test_update_1(self):

		O1 = Observer_1()
		O2 = Observer_2()
		
		self.OD.observers.append(O1)
		self.OD.observers.append(O2)
		self.OD.update_observers()

		assert O1.name == 'observer_1'
		assert O2.name == 'observer_2'

	def test_add_1(self):
		
		fruit_node = Node('fruit')
		dessert_node = Node('dessert')

		self.OD.add(fruit_node)
		self.OD.add(dessert_node)

		assert self.OD.get_node('fruit') == fruit_node
		assert self.OD.get_node('dessert') == dessert_node

	def test_remove_1(self, tree_1):

		assert tree_1.get_node('fruit').name == 'fruit'
		assert tree_1.get_node('dessert').name == 'dessert'
		assert tree_1.get_node('meat').name == 'meat'

		tree_1.remove(tree_1.get_node('meat'))

		with pytest.raises(Exception):
			tree_1.get_node('meat')

	def test_iter_1(self, tree_1):

		tree_names = set()

		for tree_node in tree_1:
			tree_names.add(tree_node.name)

		assert tree_names == {'fruit', 'dessert', 'meat'}

	def test_save_1(self):

		fruit_node = Node('fruit')
		dessert_node = Node('dessert')
		self.OD.add(fruit_node)
		self.OD.add(dessert_node)

		assert self.OD.get_node('fruit').name == 'fruit'
		assert self.OD.get_node('dessert').name == 'dessert'

		self.OD.save()
		self.OD = None


		with pytest.raises(Exception):
			self.OD.get_node('fruit')

		self.OD = self.OD_type(self.filename)

		assert self.OD.get_node('fruit').name == 'fruit'
		assert self.OD.get_node('dessert').name == 'dessert'

@pytest.fixture
def tree_2():

	filename = 'temp_recipe'
	if os.path.exists(filename + '.data'):
		os.remove(filename + '.data')

	RD = Recipe_Scaffold(filename, 'Western Omlet')

	pep = Quantity_Ingredient(1, 'number', 'pepper')
	eggs = Quantity_Ingredient(3, 'number', 'eggs')
	onion = Quantity_Ingredient(0.5, 'number', 'onion')

	RD.add(pep)
	RD.add(eggs)
	RD.add(onion)

	return RD

class Test_Recipe_Interface_1():

	filename = 'temp_recipe'

	def test_init_1(self):

		if os.path.exists(self.filename + '.data'):
			os.remove(self.filename + '.data')

		# for a new file must call an exception without a name for recipe
		with pytest.raises(Exception):
			Recipe_Scaffold(self.filename)

		# should not throw exception
		Recipe_Scaffold(self.filename, 'temp')

	def test_save_1(self, tree_2):
		if os.path.exists(self.filename + '.data'):
			os.remove(self.filename + '.data')

		assert tree_2.get_node('pepper').name == 'pepper'
		assert tree_2.get_node('pepper').quantity == 1
		assert tree_2.get_node('eggs').name == 'eggs'
		assert tree_2.get_node('eggs').quantity == 3
		assert tree_2.get_node('onion').name == 'onion'
		assert tree_2.get_node('onion').quantity == 0.5

		tree_2.save()
		tree_2 = None

		new_tree = Recipe_Scaffold(self.filename)

		assert new_tree.get_node('pepper').name == 'pepper'
		assert new_tree.get_node('pepper').quantity == 1
		assert new_tree.get_node('eggs').name == 'eggs'
		assert new_tree.get_node('eggs').quantity == 3
		assert new_tree.get_node('onion').name == 'onion'
		assert new_tree.get_node('onion').quantity == 0.5

	def test_init_2(self):

		# check to make sure no name if file already exists
		if os.path.exists(self.filename + '.data'):
			os.remove(self.filename + '.data')


		RD = Recipe_Scaffold(self.filename, 'Western Omlet')
		RD.save()

		with pytest.raises(Exception):
			Recipe_Scaffold(self.filename, name='wrong name')

@pytest.fixture
def tree_3():

	filename = 'temp_recipe_3'
	if os.path.exists(filename + '.data'):
		os.remove(filename + '.data')

	RD = Recipe_Scaffold(filename, 'Waffles')

	eggs = Quantity_Ingredient(3, 'number', 'eggs')
	batter = Quantity_Ingredient(12, 'oz', 'batter')

	RD.add(eggs)
	RD.add(batter)

	return RD

class Test_Cookbook():

	filename = 'cookbook'

	def test_cookbook_save_1(self, tree_2, tree_3):

		if os.path.exists(self.filename + '.data'):
			os.remove(self.filename + '.data')

		cookbook = OD_Scaffold(self.filename)
		cookbook.add(tree_2)
		cookbook.add(tree_3)

		assert cookbook.get_node('Western Omlet').name == 'Western Omlet'
		assert cookbook.get_node('Waffles').name == 'Waffles'
		cookbook.save()

		cookbook = None

		new_cookbook = OD_Scaffold(self.filename)
		assert new_cookbook.get_node('Western Omlet').name == 'Western Omlet'
		assert new_cookbook.get_node('Waffles').name == 'Waffles'