from src.data_source.abstract_data_source import AbstractDataSource
from src.data_source.csv_data_source import CsvDataSource
from src.data_source.openweather_data_source import OpenWeatherDataSource
from src.data_source.weatherapi_data_source import WeatherApiDataSource

# Registry of all available data sources
DATA_SOURCE_CLASSES: dict[str, type[AbstractDataSource]] = {
    OpenWeatherDataSource.SOURCE_PROVIDER_NAME: OpenWeatherDataSource,
    CsvDataSource.SOURCE_PROVIDER_NAME: CsvDataSource,
    WeatherApiDataSource.SOURCE_PROVIDER_NAME: WeatherApiDataSource,

}

__all__ = [
    "AbstractDataSource",
    "DATA_SOURCE_CLASSES"
]