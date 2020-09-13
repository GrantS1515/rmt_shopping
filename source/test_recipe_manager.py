import pytest
from data.database import Node, OD_Scaffold, Recipe_Scaffold, Quantity_Ingredient
import os
from recipe_utils import Recipe_Manager

filename = 'cookbook'

@pytest.fixture
def temp_cookbook_data():

	# if os.path.exists(filename + '.data'):
	# 	os.remove(filename + '.data')

	return OD_Scaffold(filename)

def test_add_ingredient_quantity_1(temp_cookbook_data):
	RM = Recipe_Manager(temp_cookbook_data)

	RM.recipe_name = 'Western Omlet'
	RM.ingredient_name = 'Peppers'
	RM.quantity_type = 'Number'
	RM.quantity = 2

	RM.add_ingredient_quantity()

	assert RM.currRecipe.name == 'Western Omlet'
	node = RM.currRecipe.get_node('Peppers')
	assert node.quantity == 2
	assert node.quantity_type == 'Number'

@pytest.fixture
def recipe_manager_1(temp_cookbook_data):
	RM = Recipe_Manager(temp_cookbook_data)

	RM.recipe_name = 'Western Omlet'
	RM.ingredient_name = 'Peppers'
	RM.quantity_type = 'Number'
	RM.quantity = 2

	RM.add_ingredient_quantity()
	
	return RM

def test_add_recipe_1(recipe_manager_1):
	recipe_manager_1.add_recipe()

	recipe_manager_1 = None

	cookbook = OD_Scaffold(filename)

	recipe_node = cookbook.get_node('Western Omlet')
	node = recipe_node.get_node('Peppers')
	assert node.quantity == 2
	assert node.quantity_type == 'Number'

def test_add_recipe_2(recipe_manager_1):
	recipe_manager_1.add_recipe()

	recipe_manager_1 = None

	cookbook = OD_Scaffold(filename)
	RM = Recipe_Manager(cookbook)
	RM.recipe_name = 'Waffles'
	RM.ingredient_name = 'Batter'
	RM.quantity_type = 'Oz'
	RM.quantity = 5
	RM.add_ingredient_quantity()
	RM.add_recipe()


	recipe_node = cookbook.get_node('Western Omlet')
	node = recipe_node.get_node('Peppers')
	assert node.quantity == 2
	assert node.quantity_type == 'Number'

	recipe_node = cookbook.get_node('Waffles')
	node = recipe_node.get_node('Batter')
	assert node.quantity == 5
	assert node.quantity_type == 'Oz'