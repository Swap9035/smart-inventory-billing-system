from Database import conn


class Products:
    def __init__(self, name=None, description=None, price=None, quantity=None):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    # ✅ STATIC METHOD (FIXED)
    @staticmethod
    def create_table():
        curr = conn.cursor()
        curr.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                quantity INTEGER NOT NULL,
                description TEXT NOT NULL
            )
        ''')
        conn.commit()
        curr.close()

    def insert_products(self):
        curr = conn.cursor()
        curr.execute(
            "INSERT INTO products (name, price, quantity, description) VALUES (%s, %s, %s, %s)",
            (self.name, self.price, self.quantity, self.description)
        )
        conn.commit()
        curr.close()

    def update_products(self, product_id, name=None, price=None, quantity=None, description=None):
        curr = conn.cursor()

        update_fields = []
        values = []

        if name:
            update_fields.append("name = %s")
            values.append(name)

        if price is not None:
            update_fields.append("price = %s")
            values.append(price)

        if quantity is not None:
            update_fields.append("quantity = %s")
            values.append(quantity)

        if description:
            update_fields.append("description = %s")
            values.append(description)

        if not update_fields:
            print("Nothing to update")
            curr.close()
            return

        values.append(product_id)

        query = f"UPDATE products SET {', '.join(update_fields)} WHERE id = %s"
        curr.execute(query, tuple(values))

        conn.commit()
        curr.close()
        print("Product updated successfully")

    def delete_products(self, product_id):
        curr = conn.cursor()
        curr.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()
        curr.close()

    def view_products(self):
        curr = conn.cursor()
        curr.execute("SELECT * FROM products")
        products = curr.fetchall()
        curr.close()
        return products

    def view_product_id(self, product_id):
        curr = conn.cursor()
        curr.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = curr.fetchone()
        curr.close()
        return product

    def product_menu(self):
        while True:
            print("\n1. Create Table")
            print("2. Insert Product")
            print("3. Update Product")
            print("4. Delete Product")
            print("5. View All Products")
            print("6. View Product by ID")
            print("0. Exit")

            choice = input("Enter choice: ")

            if choice == '1':
                Products.create_table()   # ✅ STATIC CALL
                print("Product table created successfully")

            elif choice == '2':
                name = input("Name: ")
                description = input("Enter the product description: ")
                price = input("Enter the product price: ")
                quantity = input("Enter the product quantity: ")

                prod = Products(name, description, price, quantity)
                prod.insert_products()
                print("Product inserted successfully")

            elif choice == '3':
                pid = input("Product ID: ")
                name = input("New Name: ")
                description = input("New Description: ")
                price = input("New Price: ")
                quantity = input("New Quantity: ")

                self.update_products(pid, name, price, quantity, description)

            elif choice == '4':
                pid = input("Product ID: ")
                self.delete_products(pid)
                print("Product deleted successfully")

            elif choice == '5':
                products = self.view_products()   # ✅ FIXED FUNCTION
                for p in products:
                    print(p)

            elif choice == '6':
                pid = input("Product ID: ")
                product = self.view_product_id(pid)
                if product:
                    print(product)
                else:
                    print("Product not found")

            elif choice == '0':
                break

            else:
                print("Invalid choice")


# RUN
if __name__ == "__main__":
    app = Products()
    app.product_menu()