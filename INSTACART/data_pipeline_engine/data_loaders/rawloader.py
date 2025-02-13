from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.snowflake import Snowflake
from os import path
import pandas as pd

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load_data_from_snowflake(*args, **kwargs):
    """
    Loads data from Snowflake into a dictionary of DataFrames and stores them in a list dfs[].
    """

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    
    with Snowflake.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        tables = ['AISLES', 'DEPARTMENTS', 'INSTACART_ORDERS', 'ORDER_PRODUCTS', 'PRODUCTS']
        data = {}
        for table in tables:
            query = f"SELECT * FROM {table};"
            data[table] = loader.load(query) 
    return data 


@test
def test_output(output, *args) -> None:
    """
    Test to ensure the output is a list of dictionaries containing DataFrames.
    """
    assert isinstance(output, dict), 'Output should be a dictionary'
    assert all(isinstance(df, pd.DataFrame) for df in output.values()), 'Each value should be a DataFrame'