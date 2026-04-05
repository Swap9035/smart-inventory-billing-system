from Database import conn


class SaleItems:

    # ✅ STATIC METHOD
    @staticmethod
    def create_table():
        curr = conn.cursor()
        curr.execute('''
            CREATE TABLE IF NOT EXISTS sale_items (
                id SERIAL PRIMARY KEY,
                sale_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                CONSTRAINT fk_sale FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE,
                CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
            )
        ''')
        conn.commit()
        curr.close()