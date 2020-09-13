from recipe_utils import Recipe_Manager
import os
from data.database import OD_Scaffold

filename = 'cookbook'
# if os.path.exists(filename + '.data'):
# 	os.remove(filename + '.data')
cookbook_data = OD_Scaffold(filename)

# RM = Recipe_Manager(cookbook_data)

# RM.recipe_name = 'Waffles'
# RM.ingredient_name = 'Batter'
# RM.quantity_type = 'Oz'
# RM.quantity = 5
# RM.add_ingredient_quantity()

# RM.add_recipe()

for i in cookbook_data:
	print(i)