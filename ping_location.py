import requests

def get_current_location():
    api_url = "https://ipinfo.io/json"
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        loc = data.get("loc", "0,0").split(",")
        latitude, longitude = loc[0], loc[1]
        return float(latitude), float(longitude)
    except requests.exceptions.RequestException as e:
        print(f"Error accessing IP geolocation service: {e}")
        return None, None

def send_location_to_server(latitude, longitude):
    url = "https://better-ducks-float.loca.lt/location" #"http://127.0.0.1:5000/location"
    data = {"latitude": latitude, "longitude": longitude}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Check if the request was successful
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error sending data to server: {e}")

if __name__ == "__main__":
    lat, lon = get_current_location()
    if lat and lon:
        send_location_to_server(lat, lon)
