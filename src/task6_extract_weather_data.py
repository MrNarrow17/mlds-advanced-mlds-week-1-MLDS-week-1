import csv
import re
from typing import Any, TextIO


def clean_text(line: str) -> str:
    """
    Clean the text line by removing non-ASCII characters and fixing known issues.

    Args:
        line (str): The line of text to clean.

    Returns:
        str: The cleaned line of text.
    """
    cleaned = line.encode("ascii", "ignore").decode("ascii")
    return cleaned


def extract_weather_data(text_file: str) -> list[dict[str, Any]]:
    """
    Extract weather data from a text file using regular expressions.

    Args:
        text_file (str): Path to the text file.

    Returns:
        list of dict: A list of dictionaries with extracted weather data.

    Raises:
        FileNotFoundError: If the text file does not exist.
    """
    pattern = re.compile(
        r"Date:\s*([^\s,]+),\s*"
        r"Max Temp:\s*([-\d.]+)[°C\s]*,\s*"
        r"Min Temp:\s*([-\d.]+)[°C\s]*,\s*"
        r"Humidity:\s*(\d+)%?,\s*"
        r"Precipitation:\s*([-\d.]+)(?:mm)?"
    )

    extracted_data = []
    with open(text_file, "r", encoding="utf-8") as f:
        for line in f:
            cleaned_line = clean_text(line)
            match = pattern.search(cleaned_line)
            if match:
                date_str, max_temp_str, min_temp_str, humidity_str, precip_str = (
                    match.groups()
                )
                extracted_data.append(
                    {
                        "date": date_str,
                        "max_temperature": float(max_temp_str),
                        "min_temperature": float(min_temp_str),
                        "humidity": int(humidity_str),
                        "precipitation": float(precip_str),
                    }
                )
    return extracted_data


def save_to_csv(
    data: list[dict[str, Any]],
    filename: str | TextIO = "extracted_weather_data.csv",
) -> None:
    """
    Save extracted weather data to a CSV file.

    Args:
        data (list of dict): Extracted weather data.
        filename (str or file-like object): Name of the CSV file or a file-like object.

    Raises:
        IOError: If there is an error writing to the file.
    """
    headers = [
        "Date",
        "Max Temperature",
        "Min Temperature",
        "Humidity",
        "Precipitation",
    ]

    try:

        def write_rows(f):
            writer = csv.writer(f)
            writer.writerow(headers)
            for row in data:
                writer.writerow(
                    [
                        row.get("date"),
                        row.get("max_temperature"),
                        row.get("min_temperature"),
                        row.get("humidity"),
                        row.get("precipitation"),
                    ]
                )

        if isinstance(filename, str):
            with open(filename, "w", newline="", encoding="utf-8") as file:
                write_rows(file)
        else:
            write_rows(filename)
    except Exception as e:
        raise IOError(f"Error writing to CSV file: {e}")


if __name__ == "__main__":
    try:
        import os

        script_dir = os.path.dirname(os.path.abspath(__file__))
        txt_path = os.path.join(script_dir, "weather_report.txt")
        weather_data = extract_weather_data(txt_path)

        save_to_csv(weather_data)
        print(
            "Data has been successfully extracted and saved to extracted_weather_data.csv."
        )
    except Exception as e:
        print(f"An error occurred: {e}")
