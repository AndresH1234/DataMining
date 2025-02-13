from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.snowflake import Snowflake
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_snowflake(data: dict, **kwargs) -> None:
    """
    Export all tables from MySQL (stored in a dictionary of DataFrames) to Snowflake.
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    tables = ['AISLES', 'DEPARTMENTS', 'INSTACART_ORDERS', 'ORDER_PRODUCTS', 'PRODUCTS']
    # Load Snowflake config
    config = ConfigFileLoader(config_path, config_profile)
    database = config.get('SNOWFLAKE_DATABASE')
    schema = config.get('SNOWFLAKE_SCHEMA')

    with Snowflake.with_config(config) as loader:
        for table_name, df in data.items():
            if not isinstance(df, DataFrame):
                continue  # Ensure we're exporting only DataFrames
            
            loader.export(
                df,
                table_name=table_name,  # Use actual table name
                database=database,  # Specify database
                schema=schema,  # Specify schema
                if_exists='replace'  # Replace existing table
            )