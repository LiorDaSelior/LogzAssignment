import os

from src.polling.abstract_data_source import AbstractDataSource
from src.weather_data import WeatherData
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

class CsvDataSource(AbstractDataSource):
    def __init__(self, cities : list[str], polling_time : int):
        super().__init__(cities, polling_time, "csv_file")
        self.csv_source_path = os.getenv("LOCAL_CSV_PATH")

    def poll_city(self, city: str) -> WeatherData:
        current_df = pd.read_csv(self.csv_source_path)
        city_df = current_df[current_df["city"] == city]
        if len(city_df) == 0:
            # TODO: add custom exception
            raise Exception(f"City {city} not found")
        current_data_row = city_df.iloc[0]
        return WeatherData(city, current_data_row["temperature"], current_data_row["description"], self.source_provider_name)

if __name__ == "__main__":
    temp = CsvDataSource(cities=["Berlin", "Sydney"], polling_time=1)
    print(temp.poll_city("Berlin"))


