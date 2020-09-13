import json

class Node():

	def __init__(self, name=None, json_data=None, **kwargs):
		
		if (name == None) and (json == None):
			raise Exception('Must have data for node')

		self.observers = []

		if name != None:
			self.name = name

		if json_data != None:
			self.json_decoder(json_data)

	def __str__(self):
		return self.name

	def collide(self, other_node):
		return self

	def update_observers(self):
		for observer in self.observers:
			observer.update()

	def json_encoder(self):
		return {'is_node': True, 
			'name': self.name}

	def json_decoder(self, json_data):
		if json_data.get('is_node'):
			self.name = json_data['name']

class Quantity_Ingredient(Node):

	def __init__(self, quantity=None, quantity_type=None, name=None, json_data=None, **kwargs):
		
		super().__init__(name, json_data)

		if (name != None) and (quantity != None) and (quantity_type != None):
			self.quantity = quantity
			self.quantity_type = quantity_type

	def json_encoder(self):
		return {'is_QI': True,
			'name': self.name,
			'quantity': self.quantity,
			'quantity_type': self.quantity_type}

	def json_decoder(self, json_data):
		if json_data.get('is_QI'):
			self.name = json_data['name']
			self.quantity = json_data['quantity']
			self.quantity_type = json_data['quantity_type']

	def __str__(self):
		return str(self.quantity) + ', ' + self.quantity_type + ' of ' + self.name


class Recipe_Node(Node):

	def __init__(self, name=None, json_data=None, **kwargs):
		self.QI_list = []
		super().__init__(name=name, json_data=json_data, **kwargs)
		

	def json_encoder(self):
		
		QI_data = {}
		for QI_node in self.QI_list:
			temp = {QI_node.name: QI_node.json_encoder()}
			QI_data = {**QI_data, **temp}

		return {'is_recipe': True,
		'name': self.name,
		'QI_list': QI_data}


	def json_decoder(self, json_data):

		if json_data.get('is_recipe'):
			self.name = json_data['name']

			for name, node_info in json_data['QI_list'].items():
				self.QI_list.append(Quantity_Ingredient(json_data=node_info))

	def __str__(self):
		my_str = self.name + '\n'

		for node in self.QI_list:
			my_str += node.__str__()
			my_str += '\n'

		return my_str