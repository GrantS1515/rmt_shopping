from database import Node, OD_Scaffold, Quantity_Ingredient, Recipe_Node
import json

class Contact():

	def __init__(self, first, last):
		self.first = first
		self.last = last

	@property
	def full_name(self):
		return '{} {}'.format(self.first, self.last)

	def json_encoder(self):
		return Contact_Encoder


# print(json.dumps(c.__dict__))

class Contact_Encoder(json.JSONEncoder):

	def default(self, obj):
		if isinstance(obj, Contact):
			return {'is_contact': True, 
			'first': obj.first,
			'last': obj.last,
			'full': obj.full_name}

		return super().default(obj)

# c = Contact('John', 'Smith')
# print(json.dumps(c, cls=c.json_encoder()))

# N1 = Node('N1')
# N2 = Node('N2')
# QI1 = Quantity_Ingredient(name='QI1', quantity_type='packages', quantity=5)
# QI2 = Quantity_Ingredient(name='QI2', quantity_type='cups', quantity=7)
# R1 = Recipe_Node('R1', [QI1, QI2])

# OD1 = OD_Scaffold('temp.json')
# OD1.add(N1)
# OD1.add(N2)
# OD1.add(R1)
# OD1.save()

OD2 = OD_Scaffold('temp.json')
print(OD2.data)
# 
# for i in OD2:
# 	print(i)

# json_out = json.dumps(N1, cls=N1.json_encoder())

# json_in = json.loads(json_out)
# # print(json_in)

# N3 = Node(json_data=json_in)
# print(N3)