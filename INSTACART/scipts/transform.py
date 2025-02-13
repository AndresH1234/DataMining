import os
import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, ForeignKey, MetaData
from sqlalchemy.exc import SQLAlchemyError

# Configuración de conexión sin base de datos para crearla
USER = os.getenv("MYSQL_USER")
PASSWORD = os.getenv("MYSQL_PASSWORD")
HOST = os.getenv("MYSQL_HOST")
PORT = "3306"

# Conectar a MySQL sin especificar la base de datos para crearla
engine = create_engine(f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}")

# Crear la base de datos si no existe
db_name = os.getenv("MYSQL_INSTACARTDB")
try:
    with engine.connect() as connection:
        connection.exec_driver_sql(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Base de datos '{db_name}' creada exitosamente.")
except SQLAlchemyError as e:
    print(f"Error al crear la base de datos: {e}")
    exit(1)

# Ahora conectarse a la base de datos correcta
engine = create_engine(f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{db_name}")

# Crear metadatos y definir el esquema de la tabla
metadata = MetaData()

# Ruta relativa a los archivos dentro de la carpeta data
data_folder = os.path.join(os.path.dirname(__file__), "../data")

# Cargar los archivos CSV
try:
    df_aisles = pd.read_csv(os.path.join(data_folder, "aisles.csv"), delimiter=";")
    df_departments = pd.read_csv(os.path.join(data_folder, "departments.csv"), delimiter=";")
    df_products = pd.read_csv(os.path.join(data_folder, "products.csv"), delimiter=";")
    df_instacart_orders = pd.read_csv(os.path.join(data_folder, "instacart_orders.csv"), delimiter=";")
    df_order_products = pd.read_csv(os.path.join(data_folder, "order_products.csv"), delimiter=";")

    print("Archivos CSV cargados correctamente.")
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit(1)

# Definir las tablas con claves foráneas
aisles_table = Table(
    "AISLES", metadata,
    Column("AISLE_ID", Integer, primary_key=True),
    Column("AISLE", String(255))
)

departments_table = Table(
    "DEPARTMENTS", metadata,
    Column("DEPARTMENT_ID", Integer, primary_key=True),
    Column("DEPARTMENT", String(255))
)

products_table = Table(
    "PRODUCTS", metadata,
    Column("PRODUCT_ID", Integer, primary_key=True),
    Column("PRODUCT_NAME", String(255)),
    Column("AISLE_ID", Integer, ForeignKey("AISLES.AISLE_ID")),
    Column("DEPARTMENT_ID", Integer, ForeignKey("DEPARTMENTS.DEPARTMENT_ID"))
)

instacart_orders_table = Table(
    "INSTACART_ORDERS", metadata,
    Column("ORDER_ID", Integer),
    Column("USER_ID", Integer),
    Column("ORDER_NUMBER", Integer),
    Column("ORDER_DOW", Integer),
    Column("ORDER_HOUR_OF_DAY", Integer),
    Column("DAYS_SINCE_PRIOR_ORDER", Integer)
)

order_products_table = Table(
    "ORDER_PRODUCTS", metadata,
    Column("ORDER_ID", Integer),
    Column("PRODUCT_ID", Integer),
    Column("ADD_TO_CART_ORDER", Float),
    Column("REORDERED", Integer)
)

# Crear las tablas en la base de datos
metadata.create_all(engine)
print("Tablas creadas correctamente.")

# Deshabilitar las verificaciones de claves foráneas
connection = engine.raw_connection()
cursor = connection.cursor()
cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
print("Verificaciones de claves foráneas deshabilitadas.")
df_aisles.columns = df_aisles.columns.str.upper()
df_departments.columns = df_departments.columns.str.upper()
df_products.columns = df_products.columns.str.upper()
df_instacart_orders.columns = df_instacart_orders.columns.str.upper()
df_order_products.columns = df_order_products.columns.str.upper()

try:
    with engine.begin() as conn:
        # Insertar datos en las tablas
        print("Insertando datos en la tabla aisles...")
        df_aisles.to_sql("AISLES", con=conn, if_exists="append", index=False)

        print("Insertando datos en la tabla departments...")
        df_departments.to_sql("DEPARTMENTS", con=conn, if_exists="append", index=False)

        print("Insertando datos en la tabla products...")
        df_products.to_sql("PRODUCTS", con=conn, if_exists="append", index=False)

        print("Insertando datos en la tabla instacart_orders...")
        df_instacart_orders.to_sql("INSTACART_ORDERS", con=conn, if_exists="append", index=False)

        print("Insertando datos en la tabla order_products...")
        df_order_products.to_sql("ORDER_PRODUCTS", con=conn, if_exists="append", index=False, chunksize=1000)

    print("Datos insertados correctamente.")

except Exception as e:
    print(f"Error al insertar datos: {e}")

finally:
    # Reactivar las verificaciones de claves foráneas
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
    print("Verificaciones de claves foráneas habilitadas nuevamente.")
    cursor.close()
    connection.close()
