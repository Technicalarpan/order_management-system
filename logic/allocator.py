import json
import os
from datetime import datetime

INVENTORY_FILE = 'data/inventory.json'
ORDER_LOG_FILE = 'data/order_log.json'


def load_inventory():
    with open(INVENTORY_FILE, 'r') as f:
        return json.load(f)


def save_inventory(inventory):
    with open(INVENTORY_FILE, 'w') as f:
        json.dump(inventory, f, indent=4)


def log_order(entry):
    if not os.path.exists(ORDER_LOG_FILE):
        with open(ORDER_LOG_FILE, 'w') as f:
            json.dump([], f)
    with open(ORDER_LOG_FILE, 'r') as f:
        logs = json.load(f)
    logs.append(entry)
    with open(ORDER_LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=4)


def load_order_log():
    if not os.path.exists(ORDER_LOG_FILE):
        return []
    with open(ORDER_LOG_FILE, 'r') as f:
        return json.load(f)


def smart_allocate(city, product, quantity, inventory):
    best_score = float('inf')
    selected_wh = None

    product_prices = inventory.get('product_prices', {})
    price = product_prices.get(product, 100)  # fallback to 100 if missing

    for name, wh in inventory['warehouses'].items():
        stock = wh.get('stock', {}).get(product, 0)
        if stock >= quantity:
            wh_city = wh['city']
            if city == wh_city:
                distance = 0
            else:
                distance = inventory['city_distances'].get(city, {}).get(wh_city, float('inf'))
            score = (distance * 0.6) + (price * 0.4)
            if score < best_score:
                best_score = score
                selected_wh = name

    return selected_wh


def place_order(city, product, quantity, customer):
    inventory = load_inventory()
    product_prices = inventory.get("product_prices", {})
    price = product_prices.get(product, 100)

    if not customer.strip():
        return "⚠️ Customer name is required.", None

    wh_name = smart_allocate(city, product, quantity, inventory)

    if wh_name:
        warehouse = inventory['warehouses'][wh_name]
        stock = warehouse.setdefault('stock', {})
        stock[product] -= quantity
        save_inventory(inventory)

        entry = {
            "customer": customer,
            "product": product,
            "quantity": quantity,
            "warehouse": wh_name,
            "location": city,
            "price_per_item": price,
            "total_cost": price * quantity,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        log_order(entry)
        return f"✅ Order placed from {wh_name} ({warehouse['city']})", entry

    return "❌ Order failed: insufficient stock.", None


def restock_warehouse(warehouse, product, quantity):
    inventory = load_inventory()
    if warehouse in inventory['warehouses']:
        inventory['warehouses'][warehouse].setdefault('stock', {})
        stock = inventory['warehouses'][warehouse]['stock']
        stock[product] = stock.get(product, 0) + quantity
        save_inventory(inventory)
        return f"🔄 Restocked {quantity} units of {product} in {warehouse}."
    return "Warehouse not found."
