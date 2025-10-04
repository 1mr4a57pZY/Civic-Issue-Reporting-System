import urllib.request
import urllib.parse
import json
import time
from typing import Optional, Tuple

def geocode_location(location: str) -> Optional[Tuple[float, float]]:
    """
    Convert a text location to GPS coordinates using OpenStreetMap Nominatim API.

    Args:
        location (str): Text address or location description

    Returns:
        Optional[Tuple[float, float]]: (latitude, longitude) if successful, None if failed
    """
    if not location or not location.strip():
        return None

    # Clean up the location string
    location = location.strip()

    # Nominatim API endpoint
    base_url = "https://nominatim.openstreetmap.org/search"

    # Parameters for the API request
    params = {
        'q': location,
        'format': 'json',
        'limit': 1,
        'addressdetails': 1,
        'extratags': 0
    }

    # Encode parameters and build URL
    query_string = urllib.parse.urlencode(params)
    url = f"{base_url}?{query_string}"

    # Headers to identify our application
    headers = {
        'User-Agent': 'Civic-Report-App/1.0'
    }

    try:
        # Create request object
        req = urllib.request.Request(url, headers=headers)

        # Make the API request
        with urllib.request.urlopen(req, timeout=10) as response:
            # Read and decode response
            data = response.read().decode('utf-8')

            # Parse JSON response
            json_data = json.loads(data)

            if json_data and len(json_data) > 0:
                # Extract latitude and longitude
                lat = float(json_data[0]['lat'])
                lon = float(json_data[0]['lon'])

                print(f"✅ Geocoded '{location}' to coordinates: {lat}, {lon}")
                return (lat, lon)
            else:
                print(f"⚠️ No geocoding results found for: '{location}'")
                return None

    except urllib.error.HTTPError as e:
        print(f"⚠️ Geocoding API request failed with status code: {e.code}")
        return None
    except urllib.error.URLError as e:
        print(f"⚠️ Geocoding request failed: {e}")
        return None
    except (ValueError, KeyError) as e:
        print(f"⚠️ Error parsing geocoding response: {e}")
        return None
    except Exception as e:
        print(f"⚠️ Unexpected error during geocoding: {e}")
        return None

def geocode_with_retry(location: str, max_retries: int = 3, delay: float = 1.0) -> Optional[Tuple[float, float]]:
    """
    Geocode a location with retry logic to handle temporary API failures.

    Args:
        location (str): Text address or location description
        max_retries (int): Maximum number of retry attempts
        delay (float): Delay between retries in seconds

    Returns:
        Optional[Tuple[float, float]]: (latitude, longitude) if successful, None if failed
    """
    for attempt in range(max_retries):
        result = geocode_location(location)

        if result is not None:
            return result

        if attempt < max_retries - 1:
            print(f"Retrying geocoding in {delay} seconds... (attempt {attempt + 1}/{max_retries})")
            time.sleep(delay)

    print(f"❌ Failed to geocode '{location}' after {max_retries} attempts")
    return None

# Test function for debugging
def test_geocoding():
    """Test the geocoding functionality with sample addresses."""
    test_addresses = [
        "Hyderabad, Telangana, India",
        "Charminar, Hyderabad",
        "Hitech City, Hyderabad",
        "Secunderabad Railway Station"
    ]

    print("Testing geocoding functionality:")
    for address in test_addresses:
        coords = geocode_with_retry(address)
        if coords:
            print(f"  {address} -> {coords[0]}, {coords[1]}")
        else:
            print(f"  {address} -> Failed to geocode")
        time.sleep(1)  # Be respectful to the API

if __name__ == "__main__":
    test_geocoding()
