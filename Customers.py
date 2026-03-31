import psycopg2
from Database import conn

class Customers:
    def __init__(self, name=None, email=None, password=None, contact=None):
        self.name = name
        self.email = email
        self.password = password
        self.contact = contact

    def create_table(self):
        curr = conn.cursor()
        curr.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                contact VARCHAR(20) NOT NULL
            )
        ''')
        conn.commit()
        curr.close()

    def insert_customer(self):
        curr = conn.cursor()
        curr.execute(
            "INSERT INTO customers (name, email, password, contact) VALUES (%s, %s, %s, %s)",
            (self.name, self.email, self.password, self.contact)
        )
        conn.commit()
        curr.close()

    def update_customer(self, customer_id, name=None, contact=None, email=None, password=None):
        curr = conn.cursor()

        update_fields = []
        values = []

        if name:
            update_fields.append("name = %s")
            values.append(name)
        if contact:
            update_fields.append("contact = %s")
            values.append(contact)
        if email:
            update_fields.append("email = %s")
            values.append(email)
        if password:
            update_fields.append("password = %s")
            values.append(password)

        if not update_fields:
            print("Nothing to update")
            return

        values.append(customer_id)

        query = f"UPDATE customers SET {', '.join(update_fields)} WHERE id = %s"
        curr.execute(query, tuple(values))

        conn.commit()
        curr.close()

    def delete_customer(self, customer_id):
        curr = conn.cursor()
        curr.execute("DELETE FROM customers WHERE id = %s", (customer_id,))
        conn.commit()
        curr.close()

    def get_all_customers(self):
        curr = conn.cursor()
        curr.execute("SELECT * FROM customers")
        customers = curr.fetchall()
        curr.close()
        return customers

    def customer_menu(self):
        while True:
            print("\n1. Create Table")
            print("2. Insert Customer")
            print("3. Update Customer")
            print("4. Delete Customer")
            print("5. View All Customers")
            print("0. Exit")

            choice = input("Enter choice: ")

            if choice == '1':
                self.create_table()
                print("Customer table created successfully")

            elif choice == '2':
                name = input("Name: ")
                contact = input("Contact: ")
                email = input("Email: ")
                password = input("Password: ")

                cust = Customers(name, email, password, contact)
                cust.insert_customer()
                print("Customer inserted successfully")
            
            elif choice == '3':
                cid = input("Customer ID: ")
                name = input("New Name: ")
                contact = input("New Contact: ")
                email = input("New Email: ")
                password = input("New Password: ")

                self.update_customer(cid, name, contact, email, password)
                print("Customer updated successfully")

            elif choice == '4':
                cid = input("Customer ID: ")
                self.delete_customer(cid)
                print("Customer deleted successfully")


            elif choice == '5':
                for c in self.get_all_customers():
                    print(c)

            elif choice == '0':
                break

            else:
                print("Invalid choice")


# ✅ RUN THIS
if __name__ == "__main__":
    app = Customers()
    app.customer_menu()