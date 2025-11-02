from src.config.Config import Config, ConfigError
from src.manager.data_source_manager import DataSourceManager

def main():
    try:
        # Load and validate config
        config = Config()
    except ConfigError as e:
        print(f"Configuration error: {e}")
        return

    # Create the manager using values from config
    manager = DataSourceManager(
        source_city_map=config.source_city_map,
        polling_time=config.polling_time
    )

    # Start polling
    manager.start()


if __name__ == "__main__":
    main()