import requests

def get_message():
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        return f"Fun Fact: {data['text']}"
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"