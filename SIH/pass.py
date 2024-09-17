import requests
import json
import pandas as pd
import math

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
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = json.loads(response.text)
        
        if data['status'] == 'OK':
            location = data['results'][0]['geometry']['location']
            # Extract postal code
            postal_code = None
            for component in data['results'][0]['address_components']:
                if 'postal_code' in component['types']:
                    postal_code = component['long_name']
                    break
            return location['lat'], location['lng'], postal_code
        else:
            print("Error in geocoding:", data['status'])
            return None, None, None
    except requests.exceptions.RequestException as e:
        print("Error making request:", e)
        return None, None, None

def find_nearest_post_office(address_latitude, address_longitude, post_offices_df):
    """
    Finds the nearest post office based on Haversine distance and prints the distance between each post office and the address.

    Args:
        address_latitude (float): Latitude of the address.
        address_longitude (float): Longitude of the address.
        post_offices_df (pandas.DataFrame): DataFrame containing post office data.

    Returns:
        pandas.Series: Series representing the nearest post office's details.
    """
    # Convert latitude and longitude columns to float
    post_offices_df['Latitude'] = pd.to_numeric(post_offices_df['Latitude'], errors='coerce')
    post_offices_df['Longitude'] = pd.to_numeric(post_offices_df['Longitude'], errors='coerce')
    
    # Filter post offices with 'Delivery' as 'Delivery'
    filtered_df = post_offices_df[post_offices_df['Delivery'] == 'Delivery']
    
    # Handle missing lat/lon in the dataset
    filtered_df = filtered_df.dropna(subset=['Latitude', 'Longitude'])
    
    # Check if filtered DataFrame is not empty
    if filtered_df.empty:
        print("No post offices available for the given criteria.")
        return pd.Series()  # Return empty Series if no valid data
    
    # Calculate distances
    filtered_df['Distance'] = filtered_df.apply(
        lambda row: haversine_distance(
            address_latitude, address_longitude, row['Latitude'], row['Longitude']
        ),
        axis=1
    )
    
    # Print distance for each post office
    for index, row in filtered_df.iterrows():
        print(f"Post Office: {row['OfficeName']}, Distance: {row['Distance']:.2f} km")
    
    # Find the nearest post office
    nearest_post_office = filtered_df.loc[filtered_df['Distance'].idxmax()]
    return nearest_post_office

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the Haversine distance between two points on a sphere.

    Args:
        lat1 (float): Latitude of point 1.
        lon1 (float): Longitude of point 1.
        lat2 (float): Latitude of point 2.
        lon2 (float): Longitude of point 2.

    Returns:
        float: The distance in kilometers.
    """
    # Convert degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    r = 6371  # Earth radius in kilometers
    return c * r

# Example usage:
#address = "Urmar,Hoishiarpur,Punjab"
address = "Subhash Balli,Kishanganj,Bihar"
latitude, longitude, postal_code = get_coordinates_and_postal_code(address)

if latitude and longitude and postal_code:
    print(f"Address: {address}")
    print(f"Latitude: {latitude}")
    print(f"Longitude: {longitude}")
    print(f"Postal Code: {postal_code}")
    
    # Load post office data as strings
    post_offices_df = pd.read_csv("pincode1.csv", dtype=str)
    
    # Filter post offices by postal code
    filtered_post_offices = post_offices_df[post_offices_df['Pincode'] == postal_code]
    
    # Print filtered post office data
    if not filtered_post_offices.empty:
        for index, row in filtered_post_offices.iterrows():
            print("CircleName:", row['CircleName'])
            print("RegionName:", row['RegionName'])
            print("DivisionName:", row['DivisionName'])
            print("OfficeName:", row['OfficeName'])
            print("Pincode:", row['Pincode'])
            print("OfficeType:", row['OfficeType'])
            print("Delivery:", row['Delivery'])
            print("District:", row['District'])
            print("StateName:", row['StateName'])
            print("Latitude:", row['Latitude'])
            print("Longitude:", row['Longitude'])
            print()
        
        # Find the nearest post office
        nearest_post_office = find_nearest_post_office(latitude, longitude, filtered_post_offices)
        
        # Print nearest post office details
        if not nearest_post_office.empty:
            print("Nearest Post Office:")
            print(nearest_post_office.to_markdown(index=False, numalign="left", stralign="left"))
        else:
            print("No nearest post office found.")
    else:
        print(f"No post offices found for the postal code: {postal_code}")
else:
    print("Unable to find address information.")
