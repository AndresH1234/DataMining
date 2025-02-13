import snowflake.connector
import os

# Snowflake connection
snowflake_conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database='INSTACART_DB',
    schema='RAW'
)

# Define queries to create tables with relationships
queries = {
    'AISLES': """
        DROP TABLE IF EXISTS CLEAN.AISLES;
        CREATE TABLE CLEAN.AISLES (
            AISLE_ID INT PRIMARY KEY,
            AISLE STRING
        );
    """,
    'DEPARTMENTS': """
        DROP TABLE IF EXISTS CLEAN.DEPARTMENTS;
        CREATE TABLE CLEAN.DEPARTMENTS (
            DEPARTMENT_ID INT PRIMARY KEY,
            DEPARTMENT STRING
        );
    """,
    'INSTACART_ORDERS': """
        DROP TABLE IF EXISTS CLEAN.INSTACART_ORDERS;
        CREATE TABLE CLEAN.INSTACART_ORDERS (
            ORDER_ID INT PRIMARY KEY,
            USER_ID INT,
            ORDER_NUMBER INT,
            ORDER_DOW INT,
            ORDER_HOUR_OF_DAY INT,
            DAYS_SINCE_PRIOR_ORDER INT
        );
    """,
    'PRODUCTS': """
        DROP TABLE IF EXISTS CLEAN.PRODUCTS;
        CREATE TABLE CLEAN.PRODUCTS (
            PRODUCT_ID INT PRIMARY KEY,
            PRODUCT STRING,
            AISLE_ID INT,
            DEPARTMENT_ID INT,
            FOREIGN KEY (AISLE_ID) REFERENCES CLEAN.AISLES(AISLE_ID),
            FOREIGN KEY (DEPARTMENT_ID) REFERENCES CLEAN.DEPARTMENTS(DEPARTMENT_ID)
        );
    """,
    'ORDER_PRODUCTS': """
        DROP TABLE IF EXISTS CLEAN.ORDER_PRODUCTS;
        CREATE TABLE CLEAN.ORDER_PRODUCTS (
            ORDER_ID INT,
            PRODUCT_ID INT,
            ADD_TO_CART_ORDER INT,
            REORDERED INT,
            PRIMARY KEY (ORDER_ID, PRODUCT_ID),
            FOREIGN KEY (ORDER_ID) REFERENCES CLEAN.INSTACART_ORDERS(ORDER_ID),
            FOREIGN KEY (PRODUCT_ID) REFERENCES CLEAN.PRODUCTS(PRODUCT_ID)
        );
    """
}

# Create tables
for table, sql in queries.items():
    with snowflake_conn.cursor() as cursor:
        for statement in sql.split(';'):
            if statement.strip():
                cursor.execute(statement.strip())
                print(f"Table {table} created successfully.")
