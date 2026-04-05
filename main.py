from Database import conn
from Customers import Customers
from Products import Products
from Sales import Sales

def main_menu():
    while True:
        print("\n1. Customer Management")
        print("2. Product Management")
        print("3. Sales Management")
        print("0. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            customer = Customers()
            customer.customer_menu()
        elif choice == '2':
            product = Products()
            product.product_menu()
        elif choice == '3':
            sale = Sales()
            sale.sale_menu()
        elif choice == '4':
            print("Exiting application...")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main_menu()