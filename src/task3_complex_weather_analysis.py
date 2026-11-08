from typing import Any

try:
    from .utils import load_json
except ImportError:
    from utils import load_json


def analyze_daily_weather(
    day: dict[str, Any],
    temp_threshold: float = 30,
    wind_threshold: float = 15,
    humidity_threshold: float = 70,
) -> dict[str, Any]:
    """
    Analyze weather data for a single day.

    Args:
        day (dict): The weather data for the day.
        temp_threshold (float): The temperature threshold to determine a hot day.
        wind_threshold (float): The wind speed threshold to determine a windy day.
        humidity_threshold (float): The humidity threshold to determine uncomfortable weather.

    Returns:
        dict: A dictionary with analysis results for the day.
    """
    max_temp = day["max_temperature"]
    min_temp = day["min_temperature"]
    precipitation = day["precipitation"]
    wind_speed = day["wind_speed"]
    humidity = day["humidity"]

    return {
        "date": day["date"],
        "is_hot_day": max_temp > temp_threshold,
        "max_temperature": max_temp,
        "min_temperature": min_temp,
        "temperature_swing": max_temp - min_temp,
        "is_windy_day": wind_speed > wind_threshold,
        "wind_speed": wind_speed,
        "is_uncomfortable_day": humidity > humidity_threshold,
        "humidity": humidity,
        "is_rainy_day": precipitation > 0,
        "precipitation": precipitation,
        "weather_description": day.get("weather_description", ""),
    }


def generate_daily_report(analysis: dict[str, Any]) -> str:
    """
    Generate a detailed report based on the analysis results for a single day.

    Args:
        analysis (dict): The analysis results for the day.

    Returns:
        str: A detailed report as a string.
    """
    descriptors = []
    if analysis["is_hot_day"]:
        descriptors.append("hot day")
    if analysis["is_windy_day"]:
        descriptors.append("windy day")
    if analysis["is_uncomfortable_day"]:
        descriptors.append("uncomfortable day")
    if analysis["is_rainy_day"]:
        descriptors.append("rainy day")
    else:
        descriptors.append("no precipitation")

    desc_str = ", ".join(descriptors)
    return (
        f"Date: {analysis['date']}\n"
        f"Weather: {analysis['weather_description']}\n"
        f"Conditions: {desc_str}\n"
        f"Max {analysis['max_temperature']}°C, Min {analysis['min_temperature']}°C (swing: {analysis['temperature_swing']}°C)\n"
        f"Wind: {analysis['wind_speed']} km/h, Humidity: {analysis['humidity']}%, Precipitation: {analysis['precipitation']} mm"
    )


def summarize_weather_analysis(analyses: list[dict[str, Any]]) -> str:
    """
    Summarize the weather analysis over multiple days.

    Args:
        analyses (list of dict): A list of daily analysis results.

    Returns:
        str: A summary report as a string.
    """
    if not analyses:
        return "No weather analysis data available."

    hottest = max(analyses, key=lambda x: x["max_temperature"])
    windiest = max(analyses, key=lambda x: x["wind_speed"])
    most_humid = max(analyses, key=lambda x: x["humidity"])
    rainiest = max(analyses, key=lambda x: x["precipitation"])

    return (
        f"Weather Summary Report:\n"
        f"Hottest day: {hottest['date']} with {hottest['max_temperature']}°C\n"
        f"Windiest day: {windiest['date']} with {windiest['wind_speed']} km/h\n"
        f"Most humid day: {most_humid['date']} with {most_humid['humidity']}%\n"
        f"Rainiest day: {rainiest['date']} with {rainiest['precipitation']} mm"
    )


if __name__ == "__main__":
    try:
        import os

        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "tokyo_weather_complex.json")
        weather_data = load_json(json_path)

        analyses = [analyze_daily_weather(day) for day in weather_data["daily"]]
        for analysis in analyses:
            report = generate_daily_report(analysis)
            print(report)
            print("-" * 40)

        summary_report = summarize_weather_analysis(analyses)
        print(summary_report)

    except Exception as e:
        print(f"An error occurred: {e}")
