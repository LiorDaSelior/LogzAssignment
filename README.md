# Weather Data Poller

This project fetches weather data from multiple sources (e.g., OpenWeather API, local CSV files) and ships it to a remote endpoint as newline‑delimited JSON objects.

---

## Installation & Setup with `uv`

1. **Install `uv`**  
   On macOS / Linux:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   On Windows (PowerShell):
   ```powershell
   irm https://astral.sh/uv/install.ps1 | iex
   ```
   
    Or using PyPI:
    ```bash
   pip install uv
   ```

2. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```

3. **Sync dependencies**  
   Using `uv`, you can manage dependencies, lock them, and sync your project environment:
   ```bash
   uv sync
   ```
   This ensures your project's dependencies are aligned with the lock file.

## Configuration

   Copy the example environment file and update it with your actual values:
   
   Open the `.env` file and replace the placeholder values with your actual configuration:
   - `LOCAL_CSV_PATH`: Full path to your local CSV file containing weather data
   - `WEATHERAPI_API_KEY`: Your API key from WeatherAPI
   - `OPENWEATHER_API_KEY`: Your API key from OpenWeather
   - `LOGZ_API_TOKEN`: Your Logz.io API token for shipping data
   
   The endpoint URLs are pre-configured but can be modified if needed.

The project reads a `settings.json` file in the directory you supply. Example:

```json
{
  "source_city_map": {
    "open_weather": ["Tel Aviv", "Paris"],
    "weather_api": ["Tel Aviv"],
    "csv_file": ["Sydney", "Berlin"]
  },
  "polling_time": 5
}
```

### Explanation:

- **`source_city_map`**  
  A mapping where:
  - Keys are the source provider names matching your data source classes' `SOURCE_PROVIDER_NAME` (`weather_api`, `open_weather`, `csv_file`).
  - Values are arrays of cities (strings) to be polled by that provider.
  - Unknown keys will be filtered out automatically at runtime.

- **`polling_time`**  
  A positive integer indicating the polling interval (in seconds) used when instantiating each data source.

## Running the Application (in working directory)

```bash
uv run python -m src.main
```

### What happens:

- The `Config` class reads `settings.json` (from the folder you passed when constructing it).
- A `DataSourceManager` is created using the `source_city_map` and `polling_time` from the config.
- The manager filters invalid sources, creates the valid sources, and begins polling.
- Each `WeatherData` object is sent as newline‑delimited JSON via HTTP POST to your configured endpoint.

## Notes

- The workflow using `uv` replaces a manual `pip` + `venv` setup — `uv` handles environment creation, dependency installation, and execution.
- Use `uv sync` after modifying dependencies to ensure lock file consistency.
- If you're not adding any dependencies, you can still benefit from `uv run` for simpler environment usage.