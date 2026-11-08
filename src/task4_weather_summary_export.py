import csv
from typing import Any, TextIO

try:
    from .utils import load_json
except ImportError:
    from utils import load_json


def summarize_weather_data(data: list[dict[str, Any]]) -> dict[str, float]:
    """
    Summarize the weather data across all days.

    Args:
        data (list of dict): The daily weather data.

    Returns:
        dict: A summary of the key metrics across all days.
    """
    if not data:
        return {}

    n = len(data)
    return {
        "average_max_temp": sum(d["max_temperature"] for d in data) / n,
        "average_min_temp": sum(d["min_temperature"] for d in data) / n,
        "total_precipitation": sum(d["precipitation"] for d in data),
        "average_wind_speed": sum(d["wind_speed"] for d in data) / n,
        "average_humidity": sum(d["humidity"] for d in data) / n,
        "hot_days": sum(1 for d in data if d["max_temperature"] > 30),
        "windy_days": sum(1 for d in data if d["wind_speed"] > 15),
        "rainy_days": sum(1 for d in data if d["precipitation"] > 0),
    }


def export_to_csv(data: list[dict[str, Any]], file: str | TextIO) -> None:
    """
    Export the summarized weather data to a CSV file or file-like object.

    Args:
        data (list of dict): The daily weather data to export.
        file (str or file-like object): The name of the CSV file to save the data in, or a file-like object.
    """
    headers = [
        "Date",
        "Max Temperature",
        "Min Temperature",
        "Precipitation",
        "Wind Speed",
        "Humidity",
        "Weather Description",
        "Is Hot Day",
        "Is Windy Day",
        "Is Rainy Day",
    ]

    def write_data(writer: csv.DictWriter) -> None:
        """Helper function to write rows to the CSV.

        Args:
            writer (csv.DictWriter): The CSV writer object.
        """
        writer.writeheader()
        for day in data:
            row = {
                "Date": day.get("date"),
                "Max Temperature": day.get("max_temperature"),
                "Min Temperature": day.get("min_temperature"),
                "Precipitation": day.get("precipitation"),
                "Wind Speed": day.get("wind_speed"),
                "Humidity": day.get("humidity"),
                "Weather Description": day.get("weather_description"),
                "Is Hot Day": str(day.get("max_temperature", 0) > 30),
                "Is Windy Day": str(day.get("wind_speed", 0) > 15),
                "Is Rainy Day": str(day.get("precipitation", 0) > 0),
            }
            writer.writerow(row)

    if isinstance(file, str):
        with open(file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            write_data(writer)
    else:
        writer = csv.DictWriter(file, fieldnames=headers)
        write_data(writer)


if __name__ == "__main__":
    try:
        import os

        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "tokyo_weather_complex.json")
        weather_data = load_json(json_path)

        summary = summarize_weather_data(weather_data["daily"])

        print("Weather Data Summary:")
        for key, value in summary.items():
            print(f"{key}: {value}")

        export_to_csv(weather_data["daily"], "tokyo_weather_summary.csv")
        print("Data successfully exported to tokyo_weather_summary.csv")

    except Exception as e:
        print(f"An error occurred: {e}")
