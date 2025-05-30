import requests

def get_message():
    headers = {'User-Agent': 'TwitterYapperBot'}
    lat, lon = 40.7608, -111.8910

    # Get forecast URL
    point_url = f'https://api.weather.gov/points/{lat},{lon}'
    point_resp = requests.get(point_url, headers=headers)
    point_data = point_resp.json()
    forecast_url = point_data['properties']['forecast']

    # Get forecast data
    forecast_resp = requests.get(forecast_url, headers=headers)
    forecast = forecast_resp.json()
    periods = forecast['properties']['periods']

    # Find today's period (usually 'Today' or first period)
    today = next((p for p in periods if p['name'] == 'Today'), periods[0])

    # Try to find tonight/overnight for low
    tonight = next((p for p in periods if p['name'] in ['Tonight', 'Overnight']), None)

    # Extract data
    highest = today['temperature']
    highest_unit = today['temperatureUnit']
    wind = today['windSpeed'] + ' ' + today['windDirection']
    desc = today['detailedForecast']

    if tonight:
        lowest = tonight['temperature']
        lowest_unit = tonight['temperatureUnit']
    else:
        # Fallback: next period (tomorrow morning)
        lowest = periods[1]['temperature']
        lowest_unit = periods[1]['temperatureUnit']

    # Try to extract a weather change (e.g., rain in the afternoon)
    import re
    change_match = re.search(r'(\d+ ?%? chance of (rain|showers|thunderstorms)[^.]*)', desc, re.IGNORECASE)
    if change_match:
        weather_changes = f"Weather Changes: {change_match.group(1)}"
    else:
        weather_changes = "Weather Changes: " + desc.split('.')[1].strip() if '.' in desc else desc

    # Format output
    output = (
        "Today's Weather in SLC, UT:\n\n"
        f"Highest: {highest}°{highest_unit}\n"
        f"Lowest: {lowest}°{lowest_unit}\n"
        f"Wind Speed: {wind}\n"
        f"{weather_changes}"
    )
    return output