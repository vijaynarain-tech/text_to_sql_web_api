import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_sample_database():
    # Connect to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect('sample_business.db')
    cursor = conn.cursor()

    # Create tables
    tables = {
        'TELD_CUSTOMER': '''
            CREATE TABLE TELD_CUSTOMER (
                customer_id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                join_date DATE,
                customer_type TEXT
            )
        ''',
        'TELD_PRODUCTS': '''
            CREATE TABLE TELD_PRODUCTS (
                product_id INTEGER PRIMARY KEY,
                name TEXT,
                category TEXT,
                price REAL,
                stock_quantity INTEGER
            )
        ''',
        'TELD_ORDERS': '''
            CREATE TABLE TELD_ORDERS (
                order_id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                order_date DATE,
                total_amount REAL,
                status TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
            )
        ''',
        'TELD_ORDER_ITEMS': '''
            CREATE TABLE TELD_ORDER_ITEMS (
                item_id INTEGER PRIMARY KEY,
                order_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                unit_price REAL,
                FOREIGN KEY (order_id) REFERENCES orders(order_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        ''',
        'TELD_SUPPLIERS': '''
            CREATE TABLE TELD_SUPPLIERS (
                supplier_id INTEGER PRIMARY KEY,
                name TEXT,
                contact_person TEXT,
                email TEXT,
                phone TEXT
            )
        ''',
        'TELD_INVENTORY': '''
            CREATE TABLE TELD_INVENTORY (
                inventory_id INTEGER PRIMARY KEY,
                product_id INTEGER,
                supplier_id INTEGER,
                quantity INTEGER,
                last_restock_date DATE,
                FOREIGN KEY (product_id) REFERENCES products(product_id),
                FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
            )
        ''',
        'TELD_PROMOTIONS': '''
            CREATE TABLE TELD_PROMOTIONS (
                promotion_id INTEGER PRIMARY KEY,
                name TEXT,
                start_date DATE,
                end_date DATE,
                discount_percentage REAL
            )
        ''',
        'TELD_PRODUCT_REVIEWS': '''
            CREATE TABLE TELD_PRODUCT_REVIEWS (
                review_id INTEGER PRIMARY KEY,
                product_id INTEGER,
                customer_id INTEGER,
                rating INTEGER,
                review_text TEXT,
                review_date DATE,
                FOREIGN KEY (product_id) REFERENCES products(product_id),
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
            )
        '''
    }

    # Create all tables
    for table_name, create_query in tables.items():
        cursor.execute(create_query)

    # Generate sample data
    np.random.seed(42)
    
    # Generate customers
    customers_data = {
        'customer_id': range(1, 51),
        'name': [f'Customer {i}' for i in range(1, 51)],
        'email': [f'customer{i}@example.com' for i in range(1, 51)],
        'join_date': [(datetime.now() - timedelta(days=np.random.randint(1, 1000))).date() for _ in range(50)],
        'customer_type': np.random.choice(['Regular', 'Premium', 'VIP'], 50)
    }
    pd.DataFrame(customers_data).to_sql('TELD_CUSTOMER', conn, if_exists='append', index=False)

    # Generate products
    products_data = {
        'product_id': range(1, 51),
        'name': [f'Product {i}' for i in range(1, 51)],
        'category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Books', 'Home'], 50),
        'price': np.random.uniform(10, 1000, 50).round(2),
        'stock_quantity': np.random.randint(0, 100, 50)
    }
    pd.DataFrame(products_data).to_sql('TELD_PRODUCTS', conn, if_exists='append', index=False)

    #Generate orders
    orders_data = {
        'order_id': range(1, 51),
        'customer_id': np.random.randint(1, 51, 50),
        'order_date': [(datetime.now() - timedelta(days=np.random.randint(1, 1000))).date() for _ in range(50)],
        'total_amount': np.random.uniform(10, 1000, 50).round(2)
    }  
    pd.DataFrame(orders_data).to_sql('TELD_ORDERS', conn, if_exists='append', index=False)

    #Generate order items
    order_items_data = {
        'item_id': range(1, 51),
        'order_id': np.random.randint(1, 51, 50),
    }
    pd.DataFrame(order_items_data).to_sql('TELD_ORDER_ITEMS', conn, if_exists='append', index=False)

    #Generate suppliers
    suppliers_data = {
        'supplier_id': range(1, 51),
        'name': [f'Supplier {i}' for i in range(1, 51)],
        'contact_person': [f'Contact {i}' for i in range(1, 51)],
    } 
    pd.DataFrame(suppliers_data).to_sql('TELD_SUPPLIERS', conn, if_exists='append', index=False)

    #Generate inventory
    inventory_data = {
        'inventory_id': range(1, 51),
        'product_id': np.random.randint(1, 51, 50),
    }   
    pd.DataFrame(inventory_data).to_sql('TELD_INVENTORY', conn, if_exists='append', index=False)

    #Generate promotions
    promotions_data = {
        'promotion_id': range(1, 51),
    }
    pd.DataFrame(promotions_data).to_sql('TELD_PROMOTIONS', conn, if_exists='append', index=False)

    #Generate product reviews
    product_reviews_data = {
        'review_id': range(1, 51),
    }   
    pd.DataFrame(product_reviews_data).to_sql('TELD_PRODUCT_REVIEWS', conn, if_exists='append', index=False)    

    # Add more sample data for other tables...
    # (For brevity, I'm showing just two tables. The complete implementation would include data for all tables)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_sample_database()
    print("Sample database created successfully!") 