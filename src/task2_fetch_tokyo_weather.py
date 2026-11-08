from typing import Any

import requests

try:
    from .utils import save_to_json
except ImportError:
    from utils import save_to_json


def fetch_weather_data() -> dict[str, Any]:
    """
    Fetch the maximum temperature forecast for Tokyo using the Open-Meteo API.

    Returns:
        dict: A dictionary containing the date and the maximum temperature.

    Raises:
        requests.HTTPError: If the HTTP request returned an unsuccessful status code.
        requests.RequestException: If there was a network error.
        KeyError: If the expected data is not in the API response.
    """
    url = (
        "https://api.open-meteo.com/v1/forecast?latitude=35.6895&longitude=139.6917"
        "&daily=temperature_2m_max&timezone=Asia/Tokyo"
    )

    data = requests.get(url).json()["daily"]
    return {"date": data["time"][0], "max_temperature": data["temperature_2m_max"][0]}


if __name__ == "__main__":
    try:
        weather_data = fetch_weather_data()

        save_to_json(weather_data, "tokyo_weather.json")
        print("Data successfully saved to tokyo_weather.json")

    except Exception as e:
        print(f"An error occurred: {e}")
