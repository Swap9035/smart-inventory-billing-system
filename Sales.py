from Database import conn
from Products import Products


class Sales:
    def __init__(self, customer_id=None, date=None, total_amount=None):
        self.customer_id = customer_id
        self.date = date
        self.total_amount = total_amount

    # ✅ STATIC METHOD
    @staticmethod
    def create_table():
        curr = conn.cursor()
        curr.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id SERIAL PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                total_amount DECIMAL(10,2) NOT NULL,
                date DATE NOT NULL,
                CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
            )
        ''')
        conn.commit()
        curr.close()

    def insert_sales(self):
        curr = conn.cursor()
        curr.execute(
            "INSERT INTO sales (customer_id, total_amount, date) VALUES (%s, %s, %s)",
            (self.customer_id, self.total_amount, self.date)
        )
        conn.commit()
        curr.close()

    def update_sales(self, sale_id, customer_id=None, total_amount=None, date=None):
        curr = conn.cursor()
        curr.execute("SELECT * FROM sales WHERE id = %s", (sale_id,))
        sale = curr.fetchone()

        if not sale:
            print("Sale not found")
            curr.close()
            return

        update_fields = []
        values = []

        if customer_id:
            update_fields.append("customer_id = %s")
            values.append(customer_id)

        if total_amount is not None:
            update_fields.append("total_amount = %s")
            values.append(total_amount)

        if date:
            update_fields.append("date = %s")
            values.append(date)

        if not update_fields:
            print("No fields to update")
            curr.close()
            return

        values.append(sale_id)

        query = f"UPDATE sales SET {', '.join(update_fields)} WHERE id = %s"
        curr.execute(query, tuple(values))

        conn.commit()
        curr.close()
        print("Sale updated successfully")

    def delete_sales(self, sale_id):
        curr = conn.cursor()
        curr.execute("DELETE FROM sales WHERE id = %s", (sale_id,))
        conn.commit()
        curr.close()

    def view_sales(self):
        curr = conn.cursor()
        curr.execute("SELECT * FROM sales")
        sales = curr.fetchall()
        curr.close()
        return sales

    def view_sale_id(self, sale_id):
        curr = conn.cursor()
        curr.execute("SELECT * FROM sales WHERE id = %s", (sale_id,))
        sale = curr.fetchall()
        curr.close()
        return sale

    def generate_bill(self, sale_id):
        curr = conn.cursor()
        curr.execute("SELECT total_amount FROM sales WHERE id = %s", (sale_id,))
        result = curr.fetchone()
        curr.close()

        if result:
            return result[0]
        return 0

    def total_sale_by_date(self, start_date, end_date):
        curr = conn.cursor()
        curr.execute(
            "SELECT SUM(total_amount) FROM sales WHERE date BETWEEN %s AND %s",
            (start_date, end_date)
        )
        total = curr.fetchone()[0] or 0
        curr.close()
        return total

    def get_sales_by_customer(self, customer_id):
        curr = conn.cursor()
        curr.execute(
            "SELECT SUM(total_amount) FROM sales WHERE customer_id = %s",
            (customer_id,)
        )
        total = curr.fetchone()[0] or 0
        curr.close()
        return total

    def sale_menu(self):
        while True:
            print("\n1. Create Table")
            print("2. Insert Sale")
            print("3. Update Sale")
            print("4. Delete Sale")
            print("5. View All Sales")
            print("6. View Sale by ID")
            print("7. Generate Bill")
            print("8. Total Sales by Date Range")
            print("9. Total Sales by Customer")
            print("0. Exit")

            choice = input("Enter choice: ")

            if choice == '1':
                Sales.create_table()   # ✅ FIXED CALL
                print("Sales table created successfully")

            elif choice == '2':
                customer_id = input("Enter Customer ID: ")
                date = input("Enter sales date (YYYY-MM-DD): ")
                total_amount = input("Enter sales amount: ")

                sale = Sales(customer_id, date, total_amount)
                sale.insert_sales()
                print("Sale inserted successfully")

            elif choice == '3':
                sid = input("Sale ID: ")
                customer_id = input("New Customer ID: ")
                date = input("New Date: ")
                total_amount = input("New Total Amount: ")

                self.update_sales(sid, customer_id, total_amount, date)

            elif choice == '4':
                sid = input("Sale ID: ")
                self.delete_sales(sid)
                print("Sale deleted successfully")

            elif choice == '5':
                sales = self.view_sales()
                for s in sales:
                    print(s)

            elif choice == '6':
                sid = input("Sale ID: ")
                sale = self.view_sale_id(sid)
                print(sale if sale else "Sale not found")

            elif choice == '7':
                sid = input("Sale ID: ")
                total = self.generate_bill(sid)
                print(f"Total Amount: {total}")

            elif choice == '8':
                start = input("Start date (YYYY-MM-DD): ")
                end = input("End date (YYYY-MM-DD): ")
                total = self.total_sale_by_date(start, end)
                print(f"Total Sales: {total}")

            elif choice == '9':
                customer_id = input("Customer ID: ")
                total = self.get_sales_by_customer(customer_id)
                print(f"Total Sales: {total}")

            elif choice == '0':
                break

            else:
                print("Invalid choice")


# RUN
if __name__ == "__main__":
    app = Sales()
    app.sale_menu()