import os

from src.data_source.abstract_data_source import AbstractDataSource, PollingError
from src.weather_data import WeatherData
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

class CsvDataSource(AbstractDataSource):
    CSV_SOURCE_PATH = os.getenv("LOCAL_CSV_PATH")
    SOURCE_PROVIDER_NAME = "csv_file"

    def __init__(self, cities : list[str], polling_time : int):
        super().__init__(cities, polling_time)

    def poll_city(self, city: str) -> WeatherData:
        current_df = pd.read_csv(self.CSV_SOURCE_PATH)
        city_df = current_df[current_df["city"] == city]
        if len(city_df) == 0:
            raise PollingError(f"City {city} not found")
        return self.transform_raw_data_to_weather_data(city_df.iloc[0], city)

    def transform_raw_data_to_weather_data(self, data, city):
        return WeatherData(
            city = city,
            temperature_celsius = data["temperature"],
            description = data["description"],
            source_provider = self.SOURCE_PROVIDER_NAME,
        )

if __name__ == "__main__":
    temp = CsvDataSource(cities=["Berlin", "Sydney"], polling_time=1)
    print(temp.poll_city("Berlin"))


