import requests
import json

# Your Google API Key
API_KEY = 'AIzaSyBZlpDfwVnYL1pTjI3SxKtEVm1chTRlT3o'

def get_coordinates_and_postal_code(address):
    """
    Gets latitude, longitude, and postal code from an address using Google Maps Geocoding API.
    
    Args:
        address (str): The address to geocode.
        
    Returns:
        tuple: A tuple containing (latitude, longitude, postal_code). If the geocoding fails, returns (None, None, None).
    """
    
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': address,
        'key': API_KEY  # Replace with your Google Maps API key
    }
    
    try:
        # Geocoding request
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = json.loads(response.text)

        if data['status'] == 'OK':
            location = data['results'][0]['geometry']['location']
            
            # Reverse geocode to get postal code for the most specific address
            reverse_geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
            reverse_params = {
                'latlng': f"{location['lat']},{location['lng']}",
                'key': API_KEY
            }
            reverse_response = requests.get(reverse_geocode_url, params=reverse_params)
            reverse_response.raise_for_status()  # Raise an exception for HTTP errors
            reverse_data = json.loads(reverse_response.text)

            if reverse_data['status'] == 'OK':
                # Find the postal code for the most specific location result
                for result in reverse_data['results']:
                    for component in result['address_components']:
                        if 'postal_code' in component['types']:
                            postal_code = component['short_name']
                            return location['lat'], location['lng'], postal_code
                # Return None for postal_code if not found
                return location['lat'], location['lng'], None
            else:
                print("Error in reverse geocoding:", reverse_data['status'])
                return None, None, None
        else:
            print("Error in geocoding:", data['status'])
            return None, None, None
    except requests.exceptions.RequestException as e:
        print("Error making request:", e)
        return None, None, None

# Example usage:
#address = "Mid Town apartments,SK Store/f-sector,Itanagr,Arunachal Pradesh"
#address = "New ND-25/7 JKPM COlony Dist Rayagada Odiasha"
#address = "Dilbagh nagar, Jalandhar, Punjab"
#address = "Tota street ,Navrangpur ,Odiasha"
#address = "Football chock ,Jalandhar,Punjab"
address = "Urar,Hoishiarpur,Punjab"
#address =  "Lovely Professional University"
latitude, longitude, postal_code = get_coordinates_and_postal_code(address)
if latitude and longitude:
    print("Latitude:", latitude)
    print("Longitude:", longitude)
    print("Postal Code:", postal_code if postal_code else "Postal code not found")
else:
    print("Unable to find address information.")
