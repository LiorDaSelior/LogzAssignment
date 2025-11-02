from src.data_source.abstract_data_source import AbstractDataSource
from src.data_source.csv_data_source import CsvDataSource
from src.data_source.openweather_data_source import OpenWeatherDataSource

# Registry of all available data sources
DATA_SOURCE_CLASSES: dict[str, type[AbstractDataSource]] = {
    OpenWeatherDataSource.SOURCE_PROVIDER_NAME: OpenWeatherDataSource,
    CsvDataSource.SOURCE_PROVIDER_NAME: CsvDataSource,
}

__all__ = [
    "AbstractDataSource",
    "OpenWeatherDataSource",
    "CsvDataSource",
    "DATA_SOURCE_CLASSES",
]