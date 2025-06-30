import streamlit as st
import pandas as pd
from logic.allocator import place_order, load_inventory, load_order_log, restock_warehouse
from logic.utils import get_products, get_cities, get_warehouses
from io import BytesIO
import base64

# Load inventory once
inventory = load_inventory()
product_prices = inventory.get("product_prices", {})

st.set_page_config(page_title="Order Manager Pro", layout="centered")
st.title("📦 Flipkart-style Order Manager")

tab1, tab2, tab3 = st.tabs(["Place Order", "Restock", "Analytics"])

# -------------------------------
# 🧾 PLACE ORDER TAB
# -------------------------------
with tab1:
    st.header("📥 Place Order")

    products = get_products(inventory)
    cities = get_cities(inventory)
    warehouses = get_warehouses(inventory)

    name = st.text_input("Customer Name")
    city = st.selectbox("City", cities)
    product = st.selectbox("Product", products)
    quantity = st.number_input("Quantity", min_value=1, step=1)

    unit_price = product_prices.get(product, 0)
    st.markdown(f"💰 **Unit Price:** ₹{unit_price}")

    total_available = sum(
        inventory["warehouses"][wh].get("stock", {}).get(product, 0)
        for wh in warehouses
        if inventory["warehouses"][wh]["city"] == city
    )

    if total_available == 0:
        st.warning("❌ Item not available in selected city.")
    else:
        st.info(f"✅ Available Stock in {city}: {total_available} units")

    with st.form("order_form"):
        submit = st.form_submit_button("Place Order")

        if submit:
            if not name.strip():
                st.error("⚠️ Please enter a customer name. Order was not placed.")
            elif total_available == 0:
                st.error("🚫 Cannot place order. Product is out of stock.")
            elif quantity > total_available:
                st.error("🚫 Quantity exceeds available stock.")
            else:
                result, details = place_order(city, product, quantity, name.strip())
                st.success(result)

                if details:
                    st.markdown("### 🧾 Invoice")
                    invoice_html = f"""
                    <div style="border: 2px solid #3498db; padding: 20px; border-radius: 10px; background-color: #f9f9f9; font-family: 'Segoe UI', sans-serif;">
                        <h2 style="color: #2c3e50;">Invoice</h2>
                        <p><strong>Customer:</strong> {details['customer']}</p>
                        <p><strong>Product:</strong> {details['product']}</p>
                        <p><strong>Quantity:</strong> {details['quantity']}</p>
                        <p><strong>Unit Price:</strong> ₹{product_prices.get(details['product'], 0)}</p>
                        <p><strong>Total Cost:</strong> <span style="color: #27ae60;"><strong>₹{details['quantity'] * product_prices.get(details['product'], 0)}</strong></span></p>
                        <p><strong>Warehouse:</strong> {details['warehouse']} ({details['location']})</p>
                        <p><strong>Date:</strong> {details['date']}</p>
                    </div>
                    """
                    st.markdown(invoice_html, unsafe_allow_html=True)

                    html_invoice = f"""
                    <html><head><style>body{{font-family:'Segoe UI'}}.highlight{{color:#27ae60;font-weight:bold}}</style></head><body>
                    <div class="invoice-box" style="border:2px solid #3498db; padding:20px; border-radius:10px;">
                        <h2>Invoice</h2>
                        <p><strong>Customer:</strong> {details['customer']}</p>
                        <p><strong>Product:</strong> {details['product']}</p>
                        <p><strong>Quantity:</strong> {details['quantity']}</p>
                        <p><strong>Unit Price:</strong> ₹{product_prices.get(details['product'], 0)}</p>
                        <p><strong>Total Cost:</strong> <span class="highlight">₹{details['quantity'] * product_prices.get(details['product'], 0)}</span></p>
                        <p><strong>Warehouse:</strong> {details['warehouse']} ({details['location']})</p>
                        <p><strong>Date:</strong> {details['date']}</p>
                    </div></body></html>
                    """
                    buffer = BytesIO(html_invoice.encode("utf-8"))
                    b64 = base64.b64encode(buffer.read()).decode()
                    href = f'<a href="data:text/html;base64,{b64}" download="invoice_{details["customer"]}.html">📥 <strong>Download Invoice</strong></a>'
                    st.markdown(href, unsafe_allow_html=True)

# -------------------------------
# 🔄 RESTOCK TAB
# -------------------------------
with tab2:
    inventory = load_inventory()
    st.header("🔄 Restock Inventory")

    st.subheader("📋 Current Stock Overview")
    stock_data = []
    for wh in get_warehouses(inventory):
        city = inventory["warehouses"][wh]["city"]
        for prod in get_products(inventory):
            qty = inventory["warehouses"][wh].get("stock", {}).get(prod, 0)
            stock_data.append({
                "City": city,
                "Warehouse": wh,
                "Product": prod,
                "Available Stock": qty
            })
    stock_df = pd.DataFrame(stock_data)
    st.dataframe(stock_df)

    st.subheader("➕ Add Stock")

    warehouse_display = {
        wh: f"{inventory['warehouses'][wh]['city']} ({wh})" for wh in get_warehouses(inventory)
    }
    display_to_wh = {v: k for k, v in warehouse_display.items()}

    with st.form("restock_form"):
        selected_display = st.selectbox("Warehouse", list(warehouse_display.values()), key="wh_restock")
        warehouse = display_to_wh[selected_display]
        product = st.selectbox("Product", get_products(inventory), key="prod_restock")

        quantity = st.number_input("Restock Quantity", min_value=1, step=1, key="restock_qty")
        restock = st.form_submit_button("Restock")

        if restock:
            message = restock_warehouse(warehouse, product, quantity)
            st.success(message)
            st.rerun()

# -------------------------------
# 📊 ANALYTICS TAB
# -------------------------------
with tab3:
    st.header("📊 Order Analytics")
    logs = load_order_log()

    if logs:
        df = pd.DataFrame(logs)

        st.subheader("📋 Order History Table")
        st.dataframe(df)

        if 'location' in df.columns:
            st.subheader("Orders per City")
            city_chart = df['location'].value_counts().reset_index()
            city_chart.columns = ['City', 'Order Count']
            st.bar_chart(city_chart.set_index('City'))

        if 'product' in df.columns:
            st.subheader("Top Products Ordered")
            product_chart = df['product'].value_counts().reset_index()
            product_chart.columns = ['Product', 'Order Count']
            st.bar_chart(product_chart.set_index('Product'))

        if 'total_cost' in df.columns:
            st.subheader("Total Cost per Order")
            st.line_chart(df['total_cost'])
    else:
        st.info("No order history available yet.")
