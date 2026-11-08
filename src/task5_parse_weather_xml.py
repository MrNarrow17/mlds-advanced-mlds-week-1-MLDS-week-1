import csv
import os
import xml.etree.ElementTree as ET
from typing import Any


def parse_weather_xml(xml_file: str) -> list[dict[str, Any]]:
    """
    Parse weather data from an XML file.

    Args:
        xml_file (str): Path to the XML file.

    Returns:
        list of dict: A list of dictionaries with parsed weather data.

    Raises:
        FileNotFoundError: If the XML file does not exist.
        ET.ParseError: If the XML file is malformed.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    parsed_data = []
    for day_elem in root.findall("day"):
        day_data = {}
        for child in day_elem:
            tag = child.tag
            text = child.text.strip() if child.text else ""
            if tag == "date":
                day_data[tag] = text
            elif tag in ("temperature", "precipitation"):
                day_data[tag] = float(text)
            elif tag == "humidity":
                day_data[tag] = int(text)
            else:
                try:
                    day_data[tag] = float(text) if "." in text else int(text)
                except ValueError:
                    day_data[tag] = text
        parsed_data.append(day_data)
    return parsed_data


def save_to_csv(
    data: list[dict[str, Any]], filename: str = "parsed_weather_data.csv"
) -> None:
    """
    Save parsed weather data to a CSV file.

    Args:
        data (list of dict): Parsed weather data.
        filename (str): Name of the CSV file.

    Raises:
        IOError: If there is an error writing to the file.
    """
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Temperature", "Humidity", "Precipitation"])
            for row in data:
                writer.writerow(
                    [
                        row.get("date"),
                        row.get("temperature"),
                        row.get("humidity"),
                        row.get("precipitation"),
                    ]
                )
    except Exception as e:
        raise IOError(f"Error writing to CSV file: {e}")


if __name__ == "__main__":
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        xml_path = os.path.join(script_dir, "weather_data.xml")
        weather_data = parse_weather_xml(xml_path)

        save_to_csv(weather_data)
        print("Data has been successfully parsed and saved to parsed_weather_data.csv.")
    except Exception as e:
        print(f"An error occurred: {e}")
