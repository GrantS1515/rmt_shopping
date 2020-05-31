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
from collections import defaultdict
from kivy.clock import Clock

class IngredientsScreen(Screen):
	def __init__(self, screenmanager, **kwargs):
		super().__init__(**kwargs)
		self.add_widget(IngredientLayout(screenmanager))

class IngredientLayout(RelativeLayout):
	def __init__(self, screenmanager, **kwargs):
		super().__init__(**kwargs)

		RB = Recipe_Button(screenmanager)
		self.add_widget(RB)

		ingredient_tree = App.get_running_app().Ingredient_Tree

		view_tree = View_Tree(ingredient_tree)
		
		add_layout = Add_Ingredient_Layout()

		add_pop = Add_Ingredient_Popup(add_layout)

		# add remaining elements to the popup
		cancel_button = Cancel_Popup_Button(add_pop)
		add_layout.add_widget(cancel_button)
		text_input = Text_Input_Popup()
		add_layout.add_widget(text_input)

		ok_pop_button = Ok_Popup_Button(add_pop, text_input, view_tree, ingredient_tree)
		add_layout.add_widget(ok_pop_button)


		add_button = Add_Ingredient_Button(add_pop)
		self.add_widget(add_button)
		
		scroller = IngredientScroller(view_tree)
		self.add_widget(scroller)

		del_ingredient = Delete_Ingredient_Button(view_tree, ingredient_tree)
		self.add_widget(del_ingredient)

class Recipe_Button(Button):

	def __init__(self, screenmanager, **kwargs):
		super().__init__(**kwargs)
		self.screenmanager = screenmanager

	def on_press(self):
		self.screenmanager.current = 'Recipe_Screen'

class IngredientScroller(ScrollView):
	def __init__(self, view_tree, **kwargs):
		super().__init__(**kwargs)

		self.view_tree = view_tree
		view_tree.size_hint_y=None
		self.view_tree.bind(minimum_height=self.view_tree.setter('height'))

		self.add_widget(self.view_tree)

class View_Tree(TreeView):

	def __init__(self, shopping_tree, **kwargs):
		super().__init__(**kwargs)
		self.tree = shopping_tree
		self.tree.observers.append(self)
		self.tree.update()

	def _build_tree(self, tree):

		name2node = defaultdict(list)
		for leaf_name in tree.bfs():
			
			leaf = tree.get_leaf(leaf_name)

			# root case
			if leaf.parents == set():
				node = TreeViewLabel(text=leaf_name)
				name2node[leaf_name].append(node)
				self.add_node(node)

			else:
				for parent_name in leaf.parents:

					for parent_node in tuple(name2node[parent_name]):
						node = TreeViewLabel(text=leaf_name)
						name2node[leaf_name].append(node)
						self.add_node(node, parent_node)

	def _clear_tree(self):
		for node in list(self.iterate_all_nodes()):
			self.remove_node(node)

	def _delay(self, dt):
		pass

	def update(self, tree):
		self._clear_tree()
		Clock.schedule_once(self._delay, 0.2)
		self._build_tree(tree)

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

		node = self.view_tree.selected_node

		if node == None:
			Error_Popup('Cannot delete entire tree').open()
			return

		node.text = leaf_name	
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
		# try:
		# 	self.ingredient_tree.get_leaf(myText)
		# 	Error_Popup('Ingredient Already in Tree').open()
		# except Exception:

		if self.view_tree.selected_node == None:
			self.ingredient_tree.add(myText)
		elif self.view_tree.selected_node.text == 'Root':
			self.ingredient_tree.add(myText)
		else:
			self.ingredient_tree.add(myText, {self.view_tree.selected_node.text})
		
		self.ingredient_tree.update()
		self.ingredient_tree.save()

		# finally:
		self.popup.dismiss()

class Error_Popup(Popup):

	def __init__(self, error_text, **kwargs):
		super().__init__(**kwargs)
		self.title = 'We Have a Problem'
		self.size_hint = (0.75, 0.75)
		self.content = Label(text=error_text)

