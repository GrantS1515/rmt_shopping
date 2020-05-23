from kivy.uix.screenmanager import Screen
from kivy.uix.treeview import TreeView, TreeViewLabel

from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.button import Button

class IngredientsScreen(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		# self.add_widget(Add_Ingredient_Button())


class IngredientScroller(ScrollView):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.size_hint= (1, 0.5)
		self.pos_hint = {'y': 0.25}
		self.do_scroll_x = False

		self.myTree = tempTree()
		self.myTree.size_hint_y=None
		self.myTree.bind(minimum_height=self.myTree.setter('height'))

		self.add_widget(self.myTree)


class tempTree(TreeView):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		H0 = self.add_node(TreeViewLabel(text='H0'))
		self.add_node(TreeViewLabel(text='H1'))

		self.add_node(TreeViewLabel(text='H01'), H0)

		for i in range(2, 25):
			node_name = 'H' + str(i)
			H0 = self.add_node(TreeViewLabel(text=node_name))

	def update(self):

		for i in range(1, 3):
			node_name = 'N' + str(i)
			H0 = self.add_node(TreeViewLabel(text=node_name))


	def on_touch_down(self, touch):
		super().on_touch_down(touch)
		print(self.selected_node.text)


# class Add_Ingredient_Button(Button):

# 	def __init__(self, **kwargs):
# 		super().__init__(**kwargs)
# 		self.text = 'Add Ingredient'


# 	def on_touch_down(self, touch):
# 		super().on_touch_down(touch)
# 		print(self.parent)