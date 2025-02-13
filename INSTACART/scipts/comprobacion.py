import random
import pandas as pd
import os
import mysql.connector
import snowflake.connector

# MySQL connection
mysql_conn = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    port=os.getenv("MYSQL_PORT"),
    database="instacart_db"
)

# Snowflake connection
snowflake_conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database='INSTACART_DB',
    schema='RAW'
)

# Diccionario de tablas y sus columnas de ID
tables = {
    'AISLES': ['AISLE_ID'],
    'DEPARTMENTS': ['DEPARTMENT_ID'],
    'INSTACART_ORDERS': ['ORDER_ID', 'USER_ID'],
    'ORDER_PRODUCTS': ['ORDER_ID', 'PRODUCT_ID'],
    'PRODUCTS': ['PRODUCT_ID']
}

def get_random_id_mysql(table, id_columns):
    query = f"""
        SELECT {', '.join(id_columns)} FROM {table} ORDER BY RAND() LIMIT 1;
    """
    df = pd.read_sql(query, mysql_conn)
    return df.iloc[0].to_dict() if not df.empty else None

def get_record_by_id_mysql(table, id_columns, record_ids):
    conditions = " AND ".join([f"{col} = {record_ids[col]}" for col in id_columns])
    query = f"SELECT * FROM {table} WHERE {conditions};"
    df = pd.read_sql(query, mysql_conn)
    return df.to_dict(orient='records')[0] if not df.empty else None

def get_record_by_id_snowflake(table, id_columns, record_ids):
    conditions = " AND ".join([f"{col} = {record_ids[col]}" for col in id_columns])
    query = f"SELECT * FROM {table} WHERE {conditions};"
    df = pd.read_sql(query, snowflake_conn)
    return df.to_dict(orient='records')[0] if not df.empty else None

def compare_records(mysql_record, snowflake_record):
    return mysql_record == snowflake_record

i = 0
while(i<3):
    i += 1
    for table, id_columns in tables.items():
        record_ids = get_random_id_mysql(table, id_columns)
        
        if record_ids:
            mysql_record = get_record_by_id_mysql(table, id_columns, record_ids)
            snowflake_record = get_record_by_id_snowflake(table, id_columns, record_ids)
            
            if mysql_record and snowflake_record:
                comparison_result = compare_records(mysql_record, snowflake_record)
                print(f"\n********Comparison result for table {table}, record IDs {record_ids}: {comparison_result}********")
                if not comparison_result:
                    print(f"Record in MySQL: {mysql_record}")
                    print(f"Record in Snowflake: {snowflake_record}")
            else:
                print(f"No matching record found in Snowflake for table {table}, record IDs {record_ids}")
        else:
            print(f"No records found in MySQL table {table}")

mysql_conn.close()
snowflake_conn.close()
