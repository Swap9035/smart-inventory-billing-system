import streamlit as st
from datetime import date

from Database import conn
from Products import Products
from Customers import Customers
from Sales import Sales
from SalesItem import SaleItems


def initialize_tables():
    try:
        Customers.create_table()
        Products.create_table()
        Sales.create_table()
        SaleItems.create_table()

        curr = conn.cursor()

        # ✅ FIXED (COALESCE added to avoid NULL crash)
        curr = conn.cursor()

        curr.execute(
            "SELECT setval('customers_id_seq', COALESCE((SELECT MAX(id) FROM customers), 1))"
        )
        curr.execute(
            "SELECT setval('products_id_seq', COALESCE((SELECT MAX(id) FROM products), 1))"
        )
        curr.execute(
            "SELECT setval('sales_id_seq', COALESCE((SELECT MAX(id) FROM sales), 1))"
        )
        curr.execute(
            "SELECT setval('sale_items_id_seq', COALESCE((SELECT MAX(id) FROM sale_items), 1))"
        )

        conn.commit()
        curr.close()

        st.success("Tables initialized successfully!")

    except Exception as e:
        st.error(f"Error initializing tables: {e}")


# App Config
st.set_page_config(page_title="Sales Inventory and Billing System", layout="wide")
st.title("Sales Inventory and Billing System")


# Initialize tables
if "Initialize Tables" not in st.session_state:
    initialize_tables()
    st.session_state["Initialize Tables"] = True


# Sidebar
st.sidebar.header("Navigation")
menu_options = st.sidebar.selectbox(
    "Choose an option",
    [
        "Dashboard",
        "Customer Management",
        "Product Management",
        "Sales Management",
        "Analytics and Reports"
    ],
)


# ================= DASHBOARD =================
if menu_options == "Dashboard":
    st.header("Dashboard")

    try:
        curr = conn.cursor()

        # Counts
        curr.execute("SELECT COUNT(*) FROM customers")
        customer_count = curr.fetchone()[0]

        curr.execute("SELECT COUNT(*) FROM products")
        product_count = curr.fetchone()[0]

        curr.execute("SELECT COUNT(*) FROM sales")
        sales_count = curr.fetchone()[0]

        # ✅ BONUS: total revenue
        curr.execute("SELECT COALESCE(SUM(total_amount),0) FROM sales")
        total_revenue = curr.fetchone()[0]

        curr.close()

        # Metrics UI
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Customers", customer_count)
        col2.metric("Total Products", product_count)
        col3.metric("Total Sales", sales_count)
        col4.metric("Total Revenue", f"₹ {total_revenue}")

        st.divider()

        st.success("System running successfully 🚀")

    except Exception as e:
        st.error(f"Error fetching dashboard data: {e}")



# ================= Customer Management =================

elif menu_options == "Customer Management":
    st.header("Customer Management")

    customer_actions = st.radio(
        "Select an action:",
        ["View Customers", "Add New Customer", "Update Customer", "Delete Customer"]
    )

    # ================= VIEW =================
    if customer_actions == "View Customers":
        st.subheader("All Customers")
        try:
            customers = Customers().get_all_customers()
            if customers:
                for cust in customers:
                    st.write(f"ID: {cust[0]}, Name: {cust[1]}, Contact: {cust[2]}, Email: {cust[3]}")
            else:
                st.info("No customers found.")
        except Exception as e:
            st.error(f"Error fetching customers: {e}")

    # ================= ADD =================
    elif customer_actions == "Add New Customer":
        st.subheader("Add New Customer")

        with st.form("add_customer_form"):
            name = st.text_input("Name")
            contact = st.text_input("Contact")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            submit = st.form_submit_button("Add Customer")

            if submit:
                if name and contact and email and password:
                    try:
                        customer = Customers(name, email, password, contact)
                        customer.insert_customer()

                        st.success("Customer added successfully!")

                        curr = conn.cursor()
                        curr.execute("SELECT setval('customers_id_seq', COALESCE((SELECT MAX(id) FROM customers), 1))")
                        conn.commit()
                        curr.close()

                    except Exception as e:
                        st.error(f"Error adding customer: {e}")
                else:
                    st.warning("Please fill in all fields.")

    # ================= UPDATE =================
    elif customer_actions == "Update Customer":
        st.subheader("Update Customer")

        try:
            customers = Customers().get_all_customers()

            if customers:
                customer_ids = {
                    f"{customer[1]} (ID: {customer[0]})": customer[0]
                    for customer in customers
                }

                selected_customer = st.selectbox(
                    "Select Customer to Update",
                    list(customer_ids.keys())
                )

                if selected_customer:
                    curr = conn.cursor()
                    curr.execute(
                        "SELECT * FROM customers WHERE id = %s",
                        (customer_ids[selected_customer],)
                    )
                    cust_data = curr.fetchone()
                    curr.close()

                    if cust_data:
                        with st.form("update_customer_form"):
                            name = st.text_input("Customer Name", value=cust_data[1])
                            email = st.text_input("Email", value=cust_data[2])
                            contact = st.text_input("Contact", value=cust_data[3])
                            password = st.text_input("Password", type="password")

                            submit = st.form_submit_button("Update Customer")

                            if submit:
                                if name and email and contact:
                                    try:
                                        Customers().update_customer(
                                            customer_ids[selected_customer],
                                            name,
                                            contact,
                                            email,
                                            password
                                        )
                                        st.success("Customer updated successfully!")

                                    except Exception as e:
                                        st.error(f"Error updating customer: {e}")
            else:
                st.info("No customers available for update.")

        except Exception as e:
            st.error(f"Error fetching customers: {e}")

    # ================= DELETE =================
    elif customer_actions == "Delete Customer":
        st.subheader("Delete Customer")

        try:
            customers = Customers().get_all_customers()

            if customers:
                customer_options = {
                    f"{cust[1]} (ID: {cust[0]})": cust[0]
                    for cust in customers
                }

                selected_customer = st.selectbox(
                    "Select Customer to Delete",
                    list(customer_options.keys())
                )

                if st.button("Delete Customer"):
                    try:
                        Customers().delete_customer(customer_options[selected_customer])

                        st.success(f"Customer '{selected_customer}' deleted successfully!")

                        curr = conn.cursor()
                        curr.execute("SELECT setval('customers_id_seq', COALESCE((SELECT MAX(id) FROM customers), 1))")
                        conn.commit()
                        curr.close()

                    except Exception as e:
                        st.error(f"Error deleting customer: {e}")

            else:
                st.info("No customers available for deletion.")

        except Exception as e:
            st.error(f"Error fetching customers: {e}")


# ================= Product Management =================
elif menu_options == "Product Management":
    st.header("Product Management")

    product_actions = st.radio(
        "Select an action:",
        ["View Products", "Add New Product", "Update Product", "Delete Product"]
    )

    # ================= VIEW =================
    if product_actions == "View Products":
        st.subheader("All Products")
        try:
            products = Products().view_products()
            if products:
                for prod in products:
                    st.write(f"ID: {prod[0]}, Name: {prod[1]}, Quantity: {prod[2]}, Price: ₹{prod[3]}, Description: {prod[4]}")
            else:
                st.info("No products found.")
        except Exception as e:
            st.error(f"Error fetching products: {e}")

    # ================= ADD =================
    elif product_actions == "Add New Product":
        st.subheader("Add New Product")

        with st.form("add_product_form"):
            name = st.text_input("Name")
            quantity = st.number_input("Quantity", min_value=0, step=1)
            price = st.number_input("Price (₹)", min_value=0.0, step=0.01)
            description = st.text_area("Description")

            submit = st.form_submit_button("Add Product")

            if submit:
                if name and price >= 0 and quantity >= 0:
                    try:
                        product = Products(name, quantity, price, description)
                        product.insert_product()

                        st.success("Product added successfully!")

                        curr = conn.cursor()
                        curr.execute("SELECT setval('products_id_seq', COALESCE((SELECT MAX(id) FROM products), 1))")
                        conn.commit()
                        curr.close()

                    except Exception as e:
                        st.error(f"Error adding product: {e}")
                else:
                    st.warning("Please fill in all fields with valid values.")

    # ================= UPDATE =================
    elif product_actions == "Update Product":
        st.subheader("Update Product")

        try:
            products = Products().view_products()

            if products:
                product_ids = {
                    f"{product[1]} (ID: {product[0]})": product[0]
                    for product in products
                }

                selected_product = st.selectbox(
                    "Select Product to Update",
                    list(product_ids.keys())
                )

                if selected_product:
                    curr = conn.cursor()
                    curr.execute(
                        "SELECT * FROM products WHERE id = %s",
                        (product_ids[selected_product],)
                    )
                    product_data = curr.fetchone()
                    curr.close()

                    if product_data:
                        with st.form("update_product_form"):

                            name = st.text_input("Product Name", value=product_data[1])

                            quantity = st.number_input(
                                "Quantity",
                                min_value=0,
                                step=1,
                                value=int(product_data[2])   # ✅ FIX
                            )

                            price = st.number_input(
                                "Price (₹)",
                                min_value=0.0,
                                step=0.01,
                                value=float(product_data[3])  # ✅ FIX
                            )

                            description = st.text_area(
                                "Description",
                                value=product_data[4]
                            )

                            submit = st.form_submit_button("Update Product")

                            if submit:
                                try:
                                    Products().update_product(
                                        product_ids[selected_product],
                                        name,
                                        quantity,
                                        price,
                                        description
                                    )
                                    st.success("Product updated successfully!")

                                except Exception as e:
                                    st.error(f"Error updating product: {e}")

            else:
                st.info("No products available for update.")

        except Exception as e:
            st.error(f"Error fetching products: {e}")
    # ================= DELETE =================
    elif product_actions == "Delete Product":
        st.subheader("Delete Product")

        try:
            products = Products().view_products()

            if products:
                product_options = {
                    f"{prod[1]} (ID: {prod[0]})": prod[0]
                    for prod in products
                }

                selected_product = st.selectbox(
                    "Select Product to Delete",
                    list(product_options.keys())
                )

                if st.button("Delete Product"):
                    try:
                        Products().delete_products(product_options[selected_product])

                        st.success(f"Product '{selected_product}' deleted successfully!")

                        curr = conn.cursor()
                        curr.execute("SELECT setval('products_id_seq', COALESCE((SELECT MAX(id) FROM products), 1))")
                        conn.commit()
                        curr.close()

                    except Exception as e:
                        st.error(f"Error deleting product: {e}")

            else:
                st.info("No products available for deletion.")

        except Exception as e:
            st.error(f"Error fetching products: {e}")



# ================= Sales Management =================
elif menu_options == "Sales Management":
    st.header("Sales Management")

    sales_actions = st.radio(
        "Select an action:",
        ["View all Sales", "Add New Sale", "Delete Sale", "Generate Bill"]
    )

    # ================= VIEW =================
    if sales_actions == "View all Sales":
        st.subheader("All Sales")
        try:
            sales = Sales().view_sales()
            if sales:
                for sale in sales:
                    st.write(f"ID: {sale[0]}, Customer ID: {sale[1]}, Total Amount: ₹{sale[2]}, Date: {sale[3]}")
            else:
                st.info("No sales found.")
        except Exception as e:
            st.error(f"Error fetching sales: {e}")
    # ================= ADD =================
    elif sales_actions == "Add New Sale":
        st.subheader("Add New Sale")

        with st.form("add_sale_form"):
            customer_id = st.number_input("Customer ID", min_value=1, step=1)
            date = st.date_input("Sales Date", value=date.today())
            total_amount = st.number_input("Total Amount (₹)", min_value=0.0, step=0.01)

            submit = st.form_submit_button("Add Sale")

            if submit:
                if customer_id and total_amount >= 0:
                    try:
                        sale = Sales(customer_id, date, total_amount)
                        sale.insert_sales()

                        st.success("Sale added successfully!")

                        curr = conn.cursor()
                        curr.execute("SELECT setval('sales_id_seq', COALESCE((SELECT MAX(id) FROM sales), 1))")
                        conn.commit()
                        curr.close()

                    except Exception as e:
                        st.error(f"Error adding sale: {e}")
                else:
                    st.warning("Please fill in all fields with valid values.")
    # ================= DELETE =================
    elif sales_actions == "Delete Sale":
        st.subheader("Delete Sale")

        try:
            sales = Sales().view_sales()

            if sales:
                sale_options = {
                    f"Sale ID: {sale[0]}, Customer ID: {sale[1]}, Amount: ₹{sale[2]}": sale[0]
                    for sale in sales
                }

                selected_sale = st.selectbox(
                    "Select Sale to Delete",
                    list(sale_options.keys())
                )

                if st.button("Delete Sale"):
                    try:
                        Sales().delete_sales(sale_options[selected_sale])

                        st.success(f"Sale '{selected_sale}' deleted successfully!")

                        curr = conn.cursor()
                        curr.execute("SELECT setval('sales_id_seq', COALESCE((SELECT MAX(id) FROM sales), 1))")
                        conn.commit()
                        curr.close()

                    except Exception as e:
                        st.error(f"Error deleting sale: {e}")

            else:
                st.info("No sales available for deletion.")

        except Exception as e:
            st.error(f"Error fetching sales: {e}")

    # ================= GENERATE BILL =================    
    elif sales_actions == "Generate Bill":
        st.subheader("Generate Bill")

        try:
            sales = Sales().view_sales()

            if sales:
                sale_options = {
                    f"Sale ID: {sale[0]}, Customer ID: {sale[1]}, Amount: ₹{sale[2]}": sale[0]
                    for sale in sales
                }

                selected_sale = st.selectbox(
                    "Select Sale to Generate Bill",
                    list(sale_options.keys())
                )

                if st.button("Generate Bill"):
                    try:
                        # Fetch sale details
                        curr = conn.cursor()
                        curr.execute(
                            "SELECT s.id, c.name, s.total_amount, s.date FROM sales s JOIN customers c ON s.customer_id = c.id WHERE s.id = %s",
                            (sale_options[selected_sale],)
                        )
                        bill_data = curr.fetchone()

                        if bill_data:
                            sale_id, customer_name, total_amount, sale_date = bill_data

                            # Fetch sale items
                            curr.execute(
                                "SELECT p.name, si.quantity, si.price FROM sale_items si JOIN products p ON si.product_id = p.id WHERE si.sale_id = %s",
                                (sale_id,)
                            )
                            items = curr.fetchall()

                            # Display bill
                            st.markdown(f"### Bill for Sale ID: {sale_id}")
                            st.markdown(f"**Customer Name:** {customer_name}")
                            st.markdown(f"**Date:** {sale_date}")
                            st.markdown("**Items Purchased:**")
                            for item in items:
                                st.write(f"- {item[0]} x {item[1]} @ ₹{item[2]} each")
                            st.markdown(f"**Total Amount:** ₹{total_amount}")

                        else:
                            st.error("Sale details not found.")

                        curr.close()

                    except Exception as e:
                        st.error(f"Error generating bill: {e}")

            else:
                st.info("No sales available for bill generation.")

        except Exception as e:
            st.error(f"Error fetching sales: {e}")  

# ================= Analytics and Reports =================
elif menu_options == "Analytics and Reports":
    st.header("Analytics and Reports")

    analytics_options = st.radio(
        "Select Report:",
        [
            "Sales Summary",   # ✅ fixed spelling
            "Sales by Date Range",
            "Top Selling Products",
            "Customer Purchase History",
            "Low Stock Products"   # ✅ added comma
        ]
    )

    # ================= SALES SUMMARY =================
    if analytics_options == "Sales Summary":
        st.subheader("Sales Summary")
        try:
            curr = conn.cursor()
            curr.execute(
                "SELECT date, SUM(total_amount) FROM sales GROUP BY date ORDER BY date"
            )
            summary = curr.fetchall()
            curr.close()

            if summary:
                for record in summary:
                    st.write(f"Date: {record[0]}, Total Sales: ₹{record[1]}")
            else:
                st.info("No sales data available.")

        except Exception as e:
            st.error(f"Error fetching sales summary: {e}")

    # ================= DATE RANGE =================
    elif analytics_options == "Sales by Date Range":
        st.subheader("Sales by Date Range")

        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")

        if st.button("Generate Report"):
            try:
                curr = conn.cursor()
                curr.execute(
                    "SELECT date, SUM(total_amount) FROM sales WHERE date BETWEEN %s AND %s GROUP BY date ORDER BY date",
                    (start_date, end_date)
                )
                summary = curr.fetchall()
                curr.close()

                if summary:
                    for record in summary:
                        st.write(f"Date: {record[0]}, Total Sales: ₹{record[1]}")
                else:
                    st.info("No data in selected range.")

            except Exception as e:
                st.error(f"Error: {e}")

    # ================= TOP PRODUCTS =================
    elif analytics_options == "Top Selling Products":
        st.subheader("Top Selling Products")

        try:
            curr = conn.cursor()
            curr.execute(
                "SELECT p.name, SUM(si.quantity) FROM sale_items si JOIN products p ON si.product_id = p.id GROUP BY p.name ORDER BY SUM(si.quantity) DESC LIMIT 10"
            )
            data = curr.fetchall()
            curr.close()

            if data:
                for row in data:
                    st.write(f"{row[0]} → {row[1]} sold")
            else:
                st.info("No data available.")

        except Exception as e:
            st.error(f"Error: {e}")

    # ================= CUSTOMER HISTORY =================
    elif analytics_options == "Customer Purchase History":
        st.subheader("Customer Purchase History")

        customer_id = st.number_input("Customer ID", min_value=1, step=1)

        if st.button("Generate Report"):
            try:
                curr = conn.cursor()
                curr.execute(
                    "SELECT id, date, total_amount FROM sales WHERE customer_id = %s",
                    (customer_id,)
                )
                data = curr.fetchall()
                curr.close()

                if data:
                    for row in data:
                        st.write(f"Sale {row[0]} | {row[1]} | ₹{row[2]}")
                else:
                    st.info("No history found.")

            except Exception as e:
                st.error(f"Error: {e}")

    # ================= LOW STOCK =================
    elif analytics_options == "Low Stock Products":
        st.subheader("Low Stock Products")

        threshold = st.number_input("Threshold", min_value=0, value=5)

        if st.button("Generate Report"):
            try:
                curr = conn.cursor()
                curr.execute(
                    "SELECT name, quantity FROM products WHERE quantity <= %s",
                    (threshold,)
                )
                data = curr.fetchall()
                curr.close()

                if data:
                    for row in data:
                        st.write(f"{row[0]} → {row[1]} left")
                else:
                    st.info("No low stock products.")

            except Exception as e:
                st.error(f"Error: {e}")