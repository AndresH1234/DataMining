if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

@transformer
def transform(data, *args, **kwargs):
    """
    Realiza la limpieza, transformación y normalización de los datos.

    Args:
        data (dict): Diccionario con DataFrames cargados desde Snowflake.

    Returns:
        dict: Diccionario con DataFrames transformados.
    """
    # Extraer las tablas relevantes
    instacart_orders = data['INSTACART_ORDERS']
    order_products = data['ORDER_PRODUCTS']
    products = data['PRODUCTS']  # Asegúrate de que esta tabla esté incluida en los datos cargados.

    # 1. Limpieza y transformación de datos

    # Valores nulos
    instacart_orders['DAYS_SINCE_PRIOR_ORDER'] = instacart_orders['DAYS_SINCE_PRIOR_ORDER'].fillna(0)  # Para la primera compra
    order_products = order_products.dropna(subset=['ADD_TO_CART_ORDER']) # Eliminar registros con valores nulos en ADD_TO_CART_ORDER
    products['PRODUCT_NAME'].fillna('Desconocido', inplace=True)  # Asignar 'Desconocido' a PRODUCT_NAME nulo

    # Duplicados
    instacart_orders = instacart_orders.drop_duplicates()  # Eliminar duplicados

    # Conversión de tipos
    instacart_orders['DAYS_SINCE_PRIOR_ORDER'] = instacart_orders['DAYS_SINCE_PRIOR_ORDER'].astype(int)
    order_products['ADD_TO_CART_ORDER'] = order_products['ADD_TO_CART_ORDER'].astype(int)

    # Retornar las tablas transformadas sin combinarlas
    return {
        'AISLES': data['AISLES'],
        'DEPARTMENTS': data['DEPARTMENTS'],
        'INSTACART_ORDERS': instacart_orders,
        'ORDER_PRODUCTS': order_products,
        'PRODUCTS': products
    }

@test
def test_output(output, *args) -> None:
    """
    Prueba que la transformación se realizó correctamente.
    """
    assert isinstance(output, dict), 'El output debe ser un diccionario'
    