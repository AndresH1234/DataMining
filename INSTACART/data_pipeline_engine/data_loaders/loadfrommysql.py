from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.mysql import MySQL
import pandas as pd
from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_mysql(*args, **kwargs):
    """
    Load all tables from the MySQL database 'instacart_db' and return as a dictionary of DataFrames.
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    with MySQL.with_config(ConfigFileLoader(config_path, config_profile)) as loader:

        tables = ['AISLES', 'DEPARTMENTS', 'INSTACART_ORDERS', 'ORDER_PRODUCTS', 'PRODUCTS']
        print("Empezando a pasar tablas")
        data = {}
        for table in tables:  # Extract table names from DataFrame
            print(table)
            query = f"SELECT * FROM {table};"
            data[table] = loader.load(query)  # Load each table into a dictionary

    return data

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert isinstance(output, dict), 'Output should be a dictionary'
    assert all(isinstance(df, pd.DataFrame) for df in output.values()), 'Each value should be a DataFrame'

