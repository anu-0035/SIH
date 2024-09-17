import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv("pincode1.csv")  # Replace "post_offices.csv" with your actual file name

# Filter the data based on the pin code
pincode = 144001  # Replace with the desired pin code
filtered_data = df[df['Pincode'] == pincode]

# Print the filtered data in the desired format
for index, row in filtered_data.iterrows():
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
    print()  # Add a blank line between records for better readability
