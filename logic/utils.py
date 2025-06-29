def get_products(inventory):
    return inventory['product_list']

def get_cities(inventory):
    return list(inventory['city_distances'].keys())

def get_warehouses(inventory):
    return list(inventory['warehouses'].keys())