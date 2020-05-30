from kivy.uix.screenmanager import Screen
from kivy.uix.treeview import TreeView, TreeViewLabel

from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label

from collections import defaultdict
from kivy.app import App
from kivy.uix.popup import Popup 
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput

class IngredientsScreen(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.add_widget(IngredientLayout())
		

class IngredientLayout(RelativeLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		view_tree = View_Tree()
		
		add_layout = Add_Ingredient_Layout()

		add_pop = Add_Ingredient_Popup(add_layout)

		# add remaining elements to the popup
		cancel_button = Cancel_Popup_Button(add_pop)
		add_layout.add_widget(cancel_button)
		text_input = Text_Input_Popup()
		add_layout.add_widget(text_input)

		ingred_tree = App.get_running_app().Ingredient_Tree
		ok_pop_button = Ok_Popup_Button(add_pop, text_input, view_tree, ingred_tree)
		add_layout.add_widget(ok_pop_button)


		add_button = Add_Ingredient_Button(add_pop)
		self.add_widget(add_button)
		
		scroller = IngredientScroller(view_tree)
		self.add_widget(scroller)

		del_ingredient = Delete_Ingredient_Button(view_tree, ingred_tree)
		self.add_widget(del_ingredient)




class IngredientScroller(ScrollView):
	def __init__(self, view_tree, **kwargs):
		super().__init__(**kwargs)

		self.size_hint= (1, 0.5)
		self.pos_hint = {'y': 0.25}
		self.do_scroll_x = False

		self.view_tree = view_tree
		view_tree.size_hint_y=None
		self.view_tree.bind(minimum_height=self.view_tree.setter('height'))

		self.add_widget(self.view_tree)

class View_Tree(TreeView):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.Shopping_Tree = App.get_running_app().Ingredient_Tree
		self.Shopping_Tree.observers.append(self)
		self.Shopping_Tree.update()

	def update(self, tree):

		'''
		TODO: cannot handle the case of one node having two parents
		'''

		for i in self.iterate_all_nodes():
			# print(i.text)
			self.remove_node(i)

		for i in self.iterate_all_nodes():
			# print(i.text)
			self.remove_node(i)

		leaf_name_2_node = {}

		for leaf_name in self.Shopping_Tree.bfs():
			leaf = self.Shopping_Tree.get_leaf(leaf_name)

			view_node = TreeViewLabel(text=leaf_name)
			leaf_name_2_node[leaf_name] = view_node

			if leaf.parents != set():
				for leaf_parent_name in leaf.parents:
					self.add_node(view_node, leaf_name_2_node[leaf_parent_name])
			else:
				self.add_node(view_node, None)

class Add_Ingredient_Popup(Popup):
	def __init__(self, add_ingredient_layout, **kwargs):
		super().__init__(**kwargs)
		self.title = 'Add a New Ingredient'
		self.size_hint = (0.75, 0.75)
		self.content = add_ingredient_layout

class Add_Ingredient_Layout(RelativeLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		
class Add_Ingredient_Button(Button):

	def __init__(self, popup, **kwargs):
		super().__init__(**kwargs)
		self.popup = popup

	def on_press(self):
		self.popup.open()

class Delete_Ingredient_Button(Button):
	def __init__(self, view_tree, ingredient_tree, **kwargs):
		super().__init__(**kwargs)
		self.view_tree = view_tree
		self.ingredient_tree = ingredient_tree

	def on_press(self):

		leaf_name = self.view_tree.selected_node.text

		if leaf_name == 'Root':
			Error_Popup('Cannot delete entire tree').open()
		else:
			self.ingredient_tree.remove(leaf_name)
			self.ingredient_tree.save()
			self.ingredient_tree.update()

class Cancel_Popup_Button(Button):
	
	def __init__(self, popup, **kwargs):
		super().__init__(**kwargs)
		self.popup = popup

	def on_press(self):
		self.popup.dismiss()

class Text_Input_Popup(TextInput):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

class Ok_Popup_Button(Button):

	def __init__(self, popup, text_input, view_tree, ingredient_tree, **kwargs):
		super().__init__(**kwargs)
		self.text_input = text_input
		self.view_tree = view_tree
		self.ingredient_tree = ingredient_tree
		self.popup = popup

	def on_press(self):

		myText = self.text_input.text

		# throw and error if string is ''
		if myText == '' :
			self.popup.dismiss()
			Error_Popup('Ingredient must not be empty').open()

		# format the text
		myText = myText.lower()
		myText = myText[0].upper() + myText[1:]

		# throw an error popup when the item already exists in some other category for now
		try:
			self.ingredient_tree.get_leaf(myText)
			Error_Popup('Ingredient Already in Tree').open()
		except Exception:

			if self.view_tree.selected_node.text == 'Root':
				self.ingredient_tree.add(myText)
			else:
				self.ingredient_tree.add(myText, {self.view_tree.selected_node.text})
			self.ingredient_tree.update()
			self.ingredient_tree.save()

		finally:
			self.popup.dismiss()


class Error_Popup(Popup):

	def __init__(self, error_text, **kwargs):
		super().__init__(**kwargs)
		self.title = 'We Have a Problem'
		self.size_hint = (0.75, 0.75)
		self.content = Label(text=error_text)