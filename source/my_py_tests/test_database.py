import sys, os
sys.path.insert(0, os.path.abspath('..'))
import pytest
import database.database as db
import database.database_lib as dbl
import database.node as nd


class Observer_1():

	name = 'not assigned in observer_1'

	def update(self, odb):
		self.name = 'observer_1'

class Observer_2():

	name = 'not assigned in observer_2'

	def update(self, odb):
		self.name = 'observer_2'


@pytest.fixture
def tree_1():

	OD = db.OD_Scaffold('temp')

	fruit_node = nd.Node('fruit')
	dessert_node = nd.Node('dessert')
	meat_node = nd.Node('meat')


	OD.add(fruit_node)
	OD.add(dessert_node)
	OD.add(meat_node)

	return OD

class Test_OD_interface_1():

	filename = 'temp'
	OD = db.OD_Scaffold('temp')
	OD_type = db.OD_Scaffold

	def test_add_1(self):
		
		fruit_node = nd.Node('fruit')
		dessert_node = nd.Node('dessert')

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

		fruit_node = nd.Node('fruit')
		dessert_node = nd.Node('dessert')
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

def test_update_1():


	core_name = 'temp_core'
	if os.path.exists(core_name):
		os.remove(core_name)
	core_data = db.OD_Scaffold(core_name)

	obs_name = 'temp_observer'
	if os.path.exists(obs_name):
		os.remove(obs_name)
	obs_data = db.OD_Scaffold(obs_name)


	ing1 = nd.Node('ing1')
	ing2 = nd.Node('ing2')
	core_data.add(ing1)
	core_data.add(ing2)

	QI1 = nd.Quantity_Ingredient(quantity=1, quantity_type='cups', name='ing1')
	QI2 = nd.Quantity_Ingredient(quantity=1, quantity_type='cups', name='ing2')
	
	R1 = nd.Recipe_Node(name='R1')
	R1.QI_list.append(QI1)

	R12 = nd.Recipe_Node(name='R12')
	R12.QI_list.append(QI1)
	R12.QI_list.append(QI2)

	R2 = nd.Recipe_Node(name='R2')
	R2.QI_list.append(QI2)

	obs_data.add(R1)
	obs_data.add(R12)
	obs_data.add(R2)

	assert R1 in obs_data
	assert R12 in obs_data
	assert R2 in obs_data

	obs_data.attach_core(core_data, dbl.process_core_node_db, dbl.process_obs_recipe_ing)
	core_data.remove(ing1)
	core_data.update_observers()

	assert R1 not in obs_data
	assert R12 not in obs_data
	assert R2 in obs_data


	core_name = 'temp_core'
	if os.path.exists(core_name):
		os.remove(core_name)

	obs_name = 'temp_observer'
	if os.path.exists(obs_name):
		os.remove(obs_name)

def test_update_2():

	core_name = 'temp_core.json'
	if os.path.exists(core_name):
		os.remove(core_name)
	core_data = db.OD_Scaffold(core_name)

	obs_name = 'temp_observer.json'
	if os.path.exists(obs_name):
		os.remove(obs_name)
	obs_data = db.OD_Scaffold(obs_name)


	ing1 = nd.Node('ing1')
	ing2 = nd.Node('ing2')
	ing3 = nd.Node('ing3')
	core_data.add(ing1)
	core_data.add(ing2)
	core_data.add(ing3)

	obs_data.add(ing1)
	obs_data.add(ing2)
	obs_data.add(ing3)	

	assert ing1 in obs_data
	assert ing2 in obs_data
	assert ing3 in obs_data

	obs_data.attach_core(core_data, dbl.process_core_node_db, dbl.process_obs_node_db)
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

def test_update_3():


	core_name = 'temp_core'
	if os.path.exists(core_name):
		os.remove(core_name)
	core_data = db.OD_Scaffold(core_name)

	obs_name = 'temp_observer'
	if os.path.exists(obs_name):
		os.remove(obs_name)
	obs_data = db.OD_Scaffold(obs_name)


	qt1 = nd.Node('cups')
	qt2 = nd.Node('packages')
	core_data.add(qt1)
	core_data.add(qt2)

	QI1 = nd.Quantity_Ingredient(quantity=1, quantity_type='cups', name='ing1')
	QI2 = nd.Quantity_Ingredient(quantity=1, quantity_type='packages', name='ing2')
	
	R1 = nd.Recipe_Node(name='R1')
	R1.QI_list.append(QI1)

	R12 = nd.Recipe_Node(name='R12')
	R12.QI_list.append(QI1)
	R12.QI_list.append(QI2)

	R2 = nd.Recipe_Node(name='R2')
	R2.QI_list.append(QI2)

	obs_data.add(R1)
	obs_data.add(R12)
	obs_data.add(R2)

	assert R1 in obs_data
	assert R12 in obs_data
	assert R2 in obs_data

	obs_data.attach_core(core_data, dbl.process_core_node_db, dbl.process_obs_recipe_qtype)
	
	core_data.remove(qt1)
	core_data.update_observers()

	assert R1 not in obs_data
	assert R12 not in obs_data
	assert R2 in obs_data


	core_name = 'temp_core'
	if os.path.exists(core_name):
		os.remove(core_name)

	obs_name = 'temp_observer'
	if os.path.exists(obs_name):
		os.remove(obs_name)