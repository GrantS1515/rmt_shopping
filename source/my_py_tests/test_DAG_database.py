import sys, os
sys.path.insert(0, os.path.abspath('..'))
import pytest
import database.database as db
import database.node as nd
import database.database_lib as dbl

def remove_files(filename):
	g_str = '_graph.json'
	d_str = '_node_data.json'

	if os.path.exists(filename + g_str):
		os.remove(filename + g_str)

	if os.path.exists(filename + d_str):
		os.remove(filename + d_str)


@pytest.fixture
def OD_1():

	filename = 'DAG_temp'
	remove_files(filename)
	
	OD = db.OD_DAG(filename)

	beans = nd.Node('Beans')
	r_beans = nd.Node('Red Beans')
	b_beans = nd.Node('Black Beans')

	OD.add(beans)
	OD.add(r_beans, beans)
	OD.add(b_beans, beans)

	return OD

def test_add_1(OD_1):

	name_set = set([node.name for node in OD_1])
	assert 'Beans' in name_set
	assert 'Red Beans' in name_set
	assert 'Black Beans' in name_set

	beans = OD_1.get_node('Beans')
	r_beans = OD_1.get_node('Red Beans')
	b_beans = OD_1.get_node('Black Beans')

	assert r_beans in OD_1.successors(beans)
	assert b_beans in OD_1.successors(beans)
	assert beans in OD_1.predecessors(r_beans)
	assert beans in OD_1.predecessors(b_beans)

def test_add_2(OD_1):
	'''
	assert that adding a node that would make cyclic raises exceptions
	'''
	beans = OD_1.get_node('Beans')
	b_beans = OD_1.get_node('Black Beans')

	with pytest.raises(ValueError):
		OD_1.add(beans, b_beans)

def test_remove_1(OD_1):
	beans = OD_1.get_node('Beans')
	r_beans = OD_1.get_node('Red Beans')
	b_beans = OD_1.get_node('Black Beans')

	OD_1.remove(beans)
	name_set = set([node.name for node in OD_1])
	assert 'Beans' not in name_set
	assert 'Red Beans' in name_set
	assert 'Black Beans' in name_set

	assert beans not in OD_1.predecessors(r_beans)
	assert beans not in OD_1.predecessors(b_beans)

def test_update_1(OD_1):

	filename = 'DAG_temp_2'
	remove_files(filename)

	b_beans = nd.Node(OD_1.get_node('Black Beans').name)
	r_beans = OD_1.get_node('Red Beans')

	OD_2 = db.OD_DAG(filename)
	OD_2.add(b_beans)
	OD_2.add(r_beans)

	assert b_beans in OD_2
	assert r_beans in OD_2

	OD_2.attach_core(OD_1, process_core=dbl.process_core_node_db)
	OD_1.remove(b_beans)
	OD_1.update_observers()

	assert b_beans not in OD_2
	assert r_beans in OD_2

def test_save_1(OD_1):

	OD_1.save()

	OD_2 = db.OD_DAG(OD_1.filename)

	name_set = set([node.name for node in OD_2])
	
	assert 'Beans' in name_set
	assert 'Red Beans' in name_set
	assert 'Black Beans' in name_set

	beans = OD_2.get_node('Beans')
	r_beans = OD_2.get_node('Red Beans')
	b_beans = OD_2.get_node('Black Beans')

	assert r_beans in OD_2.successors(beans)
	assert b_beans in OD_2.successors(beans)
	assert beans in OD_2.predecessors(r_beans)
	assert beans in OD_2.predecessors(b_beans)

def test_iter(OD_1):

	beans = OD_1.get_node('Beans')
	r_beans = OD_1.get_node('Red Beans')
	b_beans = OD_1.get_node('Black Beans')
	cherry = nd.Node('Cherry')
	OD_1.add(cherry)

	i = OD_1.__iter__()
	
	next_node_name = i.__next__().name
	assert (next_node_name == beans.name) or (next_node_name == cherry.name)
	next_node_name = i.__next__().name
	assert (next_node_name == beans.name) or (next_node_name == cherry.name)

	next_node_name = i.__next__().name
	assert (next_node_name == r_beans.name) or (next_node_name == b_beans.name)
	next_node_name = i.__next__().name
	assert (next_node_name == r_beans.name) or (next_node_name == b_beans.name)