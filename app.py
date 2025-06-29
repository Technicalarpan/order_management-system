import streamlit as st
import pandas as pd
from logic.allocator import place_order, load_inventory, load_order_log, restock_warehouse
from logic.utils import get_products, get_cities, get_warehouses
from io import BytesIO
import base64

st.set_page_config(page_title="Order Manager Pro V3", layout="centered")
st.title("📦 Flipkart-style Order Manager V3")

inventory = load_inventory()
products = get_products(inventory)
cities = get_cities(inventory)
warehouses = get_warehouses(inventory)

tab1, tab2, tab3 = st.tabs(["Place Order", "Restock", "Analytics"])

# 🧾 ORDER PLACEMENT
with tab1:
    st.header("📥 Place Order")
    with st.form("order_form"):
        name = st.text_input("Customer Name")
        city = st.selectbox("City", cities)
        product = st.selectbox("Product", products)
        quantity = st.number_input("Quantity", min_value=1, step=1)
        submit = st.form_submit_button("Place Order")

        if submit:
            result, details = place_order(city, product, quantity, name)
            st.success(result)

            if details:
                st.markdown("### 🧾 Invoice")

                # Display HTML-styled invoice
                invoice_html = f"""
                <div style="border: 2px solid #3498db; padding: 20px; border-radius: 10px; background-color: #f9f9f9; font-family: 'Segoe UI', sans-serif;">
                    <h2 style="color: #2c3e50; margin-bottom: 10px;">Invoice</h2>
                    <p><strong>Customer:</strong> {details['customer']}</p>
                    <p><strong>Product:</strong> {details['product']}</p>
                    <p><strong>Quantity:</strong> {details['quantity']}</p>
                    <p><strong>Unit Price:</strong> ₹{details['price_per_item']}</p>
                    <p><strong>Total Cost:</strong> <span style="color: #27ae60; font-weight: bold;">₹{details['total_cost']}</span></p>
                    <p><strong>Warehouse:</strong> {details['warehouse']} ({details['location']})</p>
                    <p><strong>Date:</strong> {details['date']}</p>
                </div>
                """
                st.markdown(invoice_html, unsafe_allow_html=True)

                # Downloadable HTML invoice
                html_invoice = f"""
                <html>
                <head>
                    <meta charset="utf-8">
                    <title>Invoice</title>
                    <style>
                        body {{
                            font-family: 'Segoe UI', sans-serif;
                            background-color: #f9f9f9;
                            padding: 20px;
                        }}
                        .invoice-box {{
                            border: 2px solid #3498db;
                            padding: 20px;
                            border-radius: 10px;
                            background-color: #ffffff;
                            width: 600px;
                            margin: auto;
                        }}
                        .invoice-box h2 {{
                            color: #2c3e50;
                        }}
                        .invoice-box p {{
                            margin: 5px 0;
                        }}
                        .highlight {{
                            color: #27ae60;
                            font-weight: bold;
                        }}
                    </style>
                </head>
                <body>
                    <div class="invoice-box">
                        <h2>Invoice</h2>
                        <p><strong>Customer:</strong> {details['customer']}</p>
                        <p><strong>Product:</strong> {details['product']}</p>
                        <p><strong>Quantity:</strong> {details['quantity']}</p>
                        <p><strong>Unit Price:</strong> ₹{details['price_per_item']}</p>
                        <p><strong>Total Cost:</strong> <span class="highlight">₹{details['total_cost']}</span></p>
                        <p><strong>Warehouse:</strong> {details['warehouse']} ({details['location']})</p>
                        <p><strong>Date:</strong> {details['date']}</p>
                    </div>
                </body>
                </html>
                """
                buffer = BytesIO(html_invoice.encode("utf-8"))
                b64 = base64.b64encode(buffer.read()).decode()
                href = f'<a href="data:text/html;base64,{b64}" download="invoice_{details["customer"]}.html">📥 <strong>Download Styled Invoice (HTML)</strong></a>'
                st.markdown(href, unsafe_allow_html=True)

# 🔄 RESTOCKING
with tab2:
    st.header("🔄 Restock Inventory")
    with st.form("restock_form"):
        warehouse = st.selectbox("Warehouse", warehouses)
        product = st.selectbox("Product", products, key="restock_product")
        quantity = st.number_input("Restock Quantity", min_value=1, step=1, key="restock_qty")
        restock = st.form_submit_button("Restock")

        if restock:
            message = restock_warehouse(warehouse, product, quantity)
            st.success(message)

# 📊 ANALYTICS
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
