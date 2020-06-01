import pytest
from database import OD_Scaffold, Node

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