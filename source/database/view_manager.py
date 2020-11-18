import os
import database.database as db
import database.view as view

#TODO
# Raise exception if multiple OD_scaffolds found

class View_Manager():

	def __init__(self, path=None, **view_kwargs):
		'''
		Path must point a directory with data files that are all of the same data
		'''
		self.filename2dag = {}
		self.filename2dag_view = {}
		self.db_scaffold = None
		self.view_scaffold = None

		if path == None:
			path = os.getcwd()

		for file in os.listdir(path):
			if file.endswith('_graph.json'):
				filename = str(file).split('_graph.json')[0]
				currDB = db.OD_DAG(filename)
				self.filename2dag[filename] = currDB 
				self.filename2dag_view[filename] = view.View_Nodes_Scroll(currDB, **view_kwargs)

		if self.filename2dag != {}:
			self.db_scaffold = db.OD_Scaffold(filename)
			self.view_scaffold = view.View_Nodes_Scroll(self.db_scaffold, **view_kwargs)

	def update(self, core):
		for file in os.listdir(path):
			if file.endswith('_graph.json'):
				filename = str(file).splt('_graph.json')[0]

				if filename not in self.filename2dag:
					currDB = db.OD_DAG(filename)
					self.filename2dag[filename] = currDB 
					self.filename2dag_view[filename] = view.View_Nodes_Scroll(currDB)

	def __iter__(self):
		return self.data.keys().__iter__()