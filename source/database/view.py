from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout

class View_Database(RelativeLayout):
    
    def __init__(self, data, **kwargs):
        self.data = data
        self.data.observers.append(self)
        super().__init__(size_hint=(1, 1))

    @property
    def my_selected_node(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

class Viewable_TreeView(TreeView):
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self._nodestr2node = {}
        self.data = data
        self._build_view(0)
        
    def _clear_view(self):
        for tree_node in list(self.iterate_all_nodes()):
            self.remove_node(tree_node)

    def _build_view(self, dt):
        for node in self.data:
            node_str = node.__str__()
            self._nodestr2node[node_str] = node
            TV_node = TreeViewLabel(text=node_str)
            self.add_node(TV_node)

    @property
    def my_selected_node(self):
        tree_node = self.selected_node

        if tree_node == None:
            return None
        elif tree_node.text == 'Root':
            return None
        else:
            return self._nodestr2node[tree_node.text]

    def update(self):
        self._clear_view()
        Clock.schedule_once(self._build_view, 0.1)

class View_Nodes_Scaffold(View_Database):
    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)
        self.TV = Viewable_TreeView(data, **kwargs)
        self.add_widget(self.TV)
        self.update()

    @property
    def my_selected_node(self):
        return self.TV.my_selected_node

    def update(self):
        self.TV.update()

class View_Nodes_Scroll(View_Database):
    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)
        kwargs['bar_inactive_color'] = [0.7, 0.7, 0.7, 1]
        kwargs['bar_margin'] = 5
        kwargs['bar_width'] = 10
        SV = ScrollView(**kwargs)
        

        kwargs = {'size_hint': (kwargs['size_hint'][0], None)}
        self.TV = Viewable_TreeView(data, **kwargs)
        self.TV.bind(minimum_height = self.TV.setter('height'))
        SV.add_widget(self.TV)

        self.add_widget(SV)

    def update(self):
        self.TV.update()

    @property
    def my_selected_node(self):
        return self.TV.my_selected_node


class View_Recipe_Node(Label):

    def __init__(self, recipe_node, **kwargs):
        super().__init__(**kwargs)
        self.recipe_node = recipe_node
        self.recipe_node.observers.append(self)

    def update(self):
        self.text = self.recipe_node.__str__()

class View_Nodes_Modify_Quantity(View_Database):
    
    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)

        kwargs['bar_inactive_color'] = [0.7, 0.7, 0.7, 1]
        kwargs['bar_margin'] = 5
        kwargs['bar_width'] = 10
        SV = ScrollView(**kwargs)

        grid = GridLayout(cols=1, size_hint_y=None, spacing=10)
        grid.bind(minimum_height=grid.setter('height'))
    
        SV.add_widget(grid)
        self.add_widget(SV)

        self.data = data
        self.grid = grid
        self._selected = None
        self.grid_nodes = []


    def update(self):

        for gn in self.grid_nodes.copy():
            self.grid.remove_widget(gn)
            self.grid_nodes.remove(gn)

        for node in self.data:
            VN = View_Modify_Quantity_Node(self.data, node, dec_QI, inc_QI)
            self.grid.add_widget(VN)
            self.grid_nodes.append(VN)

        

    def _set_selected(self, obj, value):
        if value != None:
            self._selected = value

    @property
    def my_selected_node(self):
        return self._selected

def dec_QI(QI_node):

    if QI_node.quantity > 0:
        QI_node.quantity -= 1

def inc_QI(QI_node):
    QI_node.quantity += 1

from kivy.properties import ObjectProperty, BooleanProperty
class View_Modify_Quantity_Node(RelativeLayout):

    def __init__(self, data, node, left_func, right_func, **kwargs):
        super().__init__(**kwargs)

        self.size_hint_y = None
        self.height = 40

        left_btn = Button(text='-', size_hint=(0.1, 1), pos_hint={'x': 0, 'y': 0})
        right_btn = Button(text='+', size_hint=(0.1, 1), pos_hint={'right': 1, 'y': 0})
        self.add_widget(left_btn)
        self.add_widget(right_btn)
        left_btn.bind(on_press=self.on_left_button)
        right_btn.bind(on_press=self.on_right_button)


        node_label = Label(text=node.__str__(), size_hint=(0.9, 1), pos_hint={'center_x': 0.5, 'y': 0})
        self.add_widget(node_label)

        self.node = node
        self.left_func = left_func
        self.right_func = right_func
        self.data = data


    def on_touch_down(self, touch):

        if self.collide_point(*touch.pos):
            self.selected = self.node

        else:
            self.selected = None


        super().on_touch_down(touch)


    def on_left_button(self, value):
        self.left_func(self.node)
        self.data.update_observers()

    def on_right_button(self, value):
        self.right_func(self.node)
        self.data.update_observers()
        