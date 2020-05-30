import pytest
from tree import Tree, Leaf, Shopping_Tree

@pytest.fixture
def tree_1():
	'''
	Construct a basic tree with 5 leafs
	'''
	
	# desserts = Leaf('Desserts')
	# breads = Leaf('Breads')
	# muffin = Leaf('Muffin')
	# french_bread = Leaf('French Bread')
	# ice_cream = Leaf('Ice Cream')

	# leafs = {'Desserts': desserts, 
	# 'Breads': breads, 
	# 'Muffin': muffin,
	# 'French Bread': french_bread,
	# 'Ice Cream': ice_cream}


	tree = Tree(Leaf)

	tree.add('Desserts')
	tree.add('Breads')
	tree.add('Muffin', {'Desserts'})
	tree.add('French Bread', {'Breads'})
	tree.add('Ice Cream', {'Desserts'})

	return tree

def test_get_leaf(tree_1):
	'''
	Ensure the the tree returns leafs by name the same as they were entered
	'''
	tree = tree_1

	assert tree.get_leaf('Desserts').name == 'Desserts'
	assert tree.get_leaf('Breads').name == 'Breads'
	assert tree.get_leaf('Muffin').name == 'Muffin'
	assert tree.get_leaf('French Bread').name == 'French Bread'
	assert tree.get_leaf('Ice Cream').name == 'Ice Cream'

	# now check that exception raised when leaf does not exist in the tree
	try:
		tree.get_leaf('Does Not Exist')
		assert False 
	except:
		pass

def test_add_leaf_1(tree_1):
	'''
	Ensure the children and parent nodes are added correctly
	'''
	tree = tree_1

	# check parent is to the root
	assert tree.get_leaf('Desserts').parents == set()
	assert tree.get_leaf('Breads').parents == set()

	# check the children of the two broad categories
	assert tree.get_leaf('Desserts').children == {'Muffin', 'Ice Cream'}
	assert tree.get_leaf('Breads').children == {'French Bread'}

	# check the children point to the parents
	assert tree.get_leaf('Muffin').parents == {'Desserts'}
	assert tree.get_leaf('French Bread').parents == {'Breads'}
	assert tree.get_leaf('Ice Cream').parents == {'Desserts'}

def test_add_leaf_2(tree_1):
	'''
	Ensure that adding two parents to a node is reflected in the appropraite parent and child references
	'''
	tree = tree_1

	tree.add('Muffin', {'Breads'})

	assert tree.get_leaf('Muffin').parents == {'Desserts', 'Breads'}

	assert 'Muffin' in tree.get_leaf('Desserts').children

	assert 'Muffin' in tree.get_leaf('Breads').children

def test_remove_1(tree_1):
	'''
	Remove an edge leaf
	'''
	tree = tree_1

	tree.remove('French Bread')

	# check parent is to the root
	assert tree.get_leaf('Desserts').parents == set()
	assert tree.get_leaf('Breads').parents == set()

	# check the children of the two broad categories
	assert tree.get_leaf('Desserts').children == {'Muffin', 'Ice Cream'}
	assert tree.get_leaf('Breads').children == set()

	# check the children point to the parents
	assert tree.get_leaf('Muffin').parents == {'Desserts'}
	assert tree.get_leaf('Ice Cream').parents == {'Desserts'}

	with pytest.raises(Exception):
		tree.get_leaf('French Bread')

def test_remove_2(tree_1):
	'''
	Remove a middle node and ensure that all child nodes are deleted
	'''
	tree = tree_1
	
	tree.remove('Breads')

	# check parent is to the root
	assert tree.get_leaf('Desserts').parents == set()

	# check the children of the two broad categories
	assert tree.get_leaf('Desserts').children == {'Muffin', 'Ice Cream'}

	# check the children point to the parents
	assert tree.get_leaf('Muffin').parents == {'Desserts'}
	assert tree.get_leaf('Ice Cream').parents == {'Desserts'}

	with pytest.raises(Exception):
		tree.get_leaf('Breads')

	with pytest.raises(Exception):
		tree.get_leaf('French Bread')


def test_remove_3(tree_1):
	tree = tree_1

	tree.add('Muffin', {'Breads'})

	tree.remove('Breads')

	# check parent is to the root
	assert tree.get_leaf('Desserts').parents == set()

	# check the children of the two broad categories
	assert tree.get_leaf('Desserts').children == {'Muffin', 'Ice Cream'}

	# check the children point to the parents
	assert tree.get_leaf('Muffin').parents == {'Desserts'}
	assert tree.get_leaf('Ice Cream').parents == {'Desserts'}

	with pytest.raises(Exception):
		tree.get_leaf('Breads')

	with pytest.raises(Exception):
		tree.get_leaf('French Bread')

# def test_remove_4(tree_1):
# 	tree = tree_1

# 	tree.add('Fruit')

# 	for i in tree:
# 		print(i)
		
# 	tree.remove('Fruit')

# 	assert False

def test_iter_1(tree_1):

	tree = tree_1

	count = 0
	for tree_leaf in tree:
		count += 1

	assert count == 5

class Leaf_2(Leaf):
	def __init__(self, name, value, **kwargs):
		super().__init__(name, **kwargs)
		self.value = value

def test_init_1():
	kwargs = {'value': 5}
	tree = Tree(Leaf_2)

	tree.add('A', **kwargs)

	assert tree.get_leaf('A').value == 5

def test_root_property_1(tree_1):
	tree = tree_1

	assert tree._root_leaf_names == {'Desserts', 'Breads'}

def test_bfs_1(tree_1):

	tree = tree_1
	tree_1.add('Fruits')
	tree_1.add('Banana', {'Fruits'})
	new_tree = Tree(Leaf)

	# this works when I can make another tree without throwing an error
	for leaf_name in tree.bfs():
		new_tree.add(leaf_name, tree.get_leaf(leaf_name).parents)

	assert new_tree == tree


@pytest.fixture
def shopping_tree_1():
	tree = Shopping_Tree(Leaf, 'temp')

	tree.add('Desserts')
	tree.add('Breads')
	tree.add('Muffin', {'Desserts'})
	tree.add('French Bread', {'Breads'})
	tree.add('Ice Cream', {'Desserts'})

	return tree

def test_save_1(shopping_tree_1):
	tree = shopping_tree_1
	tree.save()
	new_tree = Shopping_Tree(Leaf, 'temp')
	assert tree == new_tree

class observer_1():

	def __init__(self):
		self.data = None

	def update(self, shopping_tree):
		self.data = shopping_tree.get_leaf('Ice Cream')

def test_observer(shopping_tree_1):
	tree = shopping_tree_1

	obs = observer_1()
	tree.observers.append(obs)

	tree.update()

	assert obs.data.name == 'Ice Cream'

	tree.remove('Ice Cream')

	with pytest.raises(Exception):
		tree.update()