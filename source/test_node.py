# import pytest
from node import Quantity_Ingredient, Node_Accumulator, Recipe_Node

def test_accumulator_1():
	QI1 = Quantity_Ingredient(5, 'Heads', 'Lettuce')
	QI2 = Quantity_Ingredient(6, 'Heads', 'Lettuce')
	QI3 = Quantity_Ingredient(5, 'Packages', 'Fruit')
	QI4 = Quantity_Ingredient(3, 'Packages', 'Gummies')

	nodes = [QI1, QI2, QI3, QI4]
	new_nodes = Node_Accumulator(nodes)

	assert len(new_nodes) == 3

	QI_A = new_nodes[0]
	QI_B = new_nodes[1]
	QI_C = new_nodes[2]

	assert QI_A.quantity == 11
	assert QI_B.quantity == 5
	assert QI_C.quantity == 3

def test_str2name_QI():
	QI1 = Quantity_Ingredient(5, 'Heads', 'Lettuce')

	assert QI1.str2name(QI1.__str__()) == 'Lettuce'

def test_str2name_RN():

	QI1 = Quantity_Ingredient(5, 'Heads', 'Lettuce')
	QI2 = Quantity_Ingredient(3, 'Packages', 'Gummies')

	RN1 = Recipe_Node(name='RN1')
	RN1.QI_list.append(QI1)
	RN1.QI_list.append(QI2)

	assert RN1.str2name(RN1.__str__()) == 'RN1'
