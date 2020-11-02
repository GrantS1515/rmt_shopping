# def consistent_names(database, node):

# 	OD_name_set = set()
# 	OD_name_set |= set([i.name for i in database])

# 	return {node.name}.issubset(OD_name_set)

# def consistent_ingredients(database, recipe_node):

# 	OD_name_set = set()
# 	OD_name_set |= set([i.name for i in database])
# 	recipe_node_ingredients = set([i.name for i in recipe_node.QI_list])

# 	return recipe_node_ingredients.issubset(OD_name_set)

# def consistent_quantity_types(database, recipe_node):

# 	OD_name_set = set()
# 	OD_name_set |= set([i.name for i in database])
# 	recipe_node_ingredients = set([i.quantity_type for i in recipe_node.QI_list])

# 	return recipe_node_ingredients.issubset(OD_name_set)

def process_core_node_db(database):
	OD_name_set = set()
	OD_name_set |= set([i.name for i in database])

	return OD_name_set

def process_obs_recipe_ing(recipe_node):
	return set([i.name for i in recipe_node.QI_list])

def process_obs_recipe_qtype(recipe_node):
	return set([i.quantity_type for i in recipe_node.QI_list])	

def process_obs_node_db(node):
	return {node.name}