import sys, os
sys.path.insert(0, os.path.abspath('..'))
import pytest
import database.node as nd

def test_accumulator_1():
	QI1 = nd.Quantity_Ingredient(5, 'Heads', 'Lettuce')
	QI2 = nd.Quantity_Ingredient(6, 'Heads', 'Lettuce')
	QI3 = nd.Quantity_Ingredient(5, 'Packages', 'Fruit')
	QI4 = nd.Quantity_Ingredient(3, 'Packages', 'Gummies')

	nodes = [QI1, QI2, QI3, QI4]
	new_nodes = nd.Node_Accumulator(nodes)

	assert len(new_nodes) == 3

	QI_A = new_nodes[0]
	QI_B = new_nodes[1]
	QI_C = new_nodes[2]

	assert QI_A.quantity == 11
	assert QI_B.quantity == 5
	assert QI_C.quantity == 3
