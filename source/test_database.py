import pytest
from database import OD_Scaffold 
from node import Node, Quantity_Ingredient, Recipe_Node
import os
from node import Node

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

from database import is_consistent_nodeOD_node, is_consistent_ingredient_OD_recipe_node
def test_update_1():


	core_name = 'temp_core.json'
	if os.path.exists(core_name):
		os.remove(core_name)
	core_data = OD_Scaffold(core_name)

	obs_name = 'temp_observer.json'
	if os.path.exists(obs_name):
		os.remove(obs_name)
	obs_data = OD_Scaffold(obs_name)


	ing1 = Node('ing1')
	ing2 = Node('ing2')
	core_data.add(ing1)
	core_data.add(ing2)

	QI1 = Quantity_Ingredient(quantity=1, quantity_type='cups', name='ing1')
	QI2 = Quantity_Ingredient(quantity=1, quantity_type='cups', name='ing2')
	
	R1 = Recipe_Node(name='R1')
	R1.QI_list.append(QI1)

	R12 = Recipe_Node(name='R12')
	R12.QI_list.append(QI1)
	R12.QI_list.append(QI2)

	R2 = Recipe_Node(name='R2')
	R2.QI_list.append(QI2)

	obs_data.add(R1)
	obs_data.add(R12)
	obs_data.add(R2)

	assert R1 in obs_data
	assert R12 in obs_data
	assert R2 in obs_data

	obs_data.attach_core(core_data, is_consistent_ingredient_OD_recipe_node)
	core_data.remove(ing1)
	core_data.update_observers()

	assert R1 not in obs_data
	assert R12 not in obs_data
	assert R2 in obs_data


	core_name = 'temp_core.json'
	if os.path.exists(core_name):
		os.remove(core_name)

	obs_name = 'temp_observer.json'
	if os.path.exists(obs_name):
		os.remove(obs_name)

def test_update_2():

	core_name = 'temp_core.json'
	if os.path.exists(core_name):
		os.remove(core_name)
	core_data = OD_Scaffold(core_name)

	obs_name = 'temp_observer.json'
	if os.path.exists(obs_name):
		os.remove(obs_name)
	obs_data = OD_Scaffold(obs_name)


	ing1 = Node('ing1')
	ing2 = Node('ing2')
	ing3 = Node('ing3')
	core_data.add(ing1)
	core_data.add(ing2)
	core_data.add(ing3)

	obs_data.add(ing1)
	obs_data.add(ing2)
	obs_data.add(ing3)	

	assert ing1 in obs_data
	assert ing2 in obs_data
	assert ing3 in obs_data

	obs_data.attach_core(core_data, is_consistent_nodeOD_node)
	core_data.remove(ing1)
	core_data.update_observers()

	assert ing1 not in obs_data
	assert ing2 in obs_data
	assert ing3 in obs_data


	core_name = 'temp_core.json'
	if os.path.exists(core_name):
		os.remove(core_name)

	obs_name = 'temp_observer.json'
	if os.path.exists(obs_name):
		os.remove(obs_name)