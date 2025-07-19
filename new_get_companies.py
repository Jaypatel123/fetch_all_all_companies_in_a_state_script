import os
import googlemaps
import time
import openpyxl
from dotenv import load_dotenv
load_dotenv()
# Your Google Maps API key
API_KEY = os.getenv('API_KEY')

gmaps = googlemaps.Client(key=API_KEY)

# Search query and location
SEARCH_QUERY = "businesses"
LOCATION = "Indiana, USA"
RADIUS = 50000  # Maximum allowed radius in meters for nearby search

# Excel setup
wb = openpyxl.Workbook()
ws = wb.active
ws.append(['Name', 'Address', 'Phone Number', 'Website'])

# To avoid duplicates
added_websites = set()

# Paginated results handling
def fetch_places(query, location):
    places_result = gmaps.places(query=query, location=location)

    while True:
        for place in places_result.get('results', []):
            place_id = place['place_id']
            details = gmaps.place(place_id=place_id)['result']

            name = details.get('name')
            address = details.get('formatted_address')
            phone = details.get('formatted_phone_number', '')
            website = details.get('website', '')

            # Avoid duplicate website entries
            if website in added_websites:
                continue
            added_websites.add(website)

            ws.append([name, address, phone, website])

        # Handle pagination
        if 'next_page_token' in places_result:
            time.sleep(2)
            places_result = gmaps.places(query=query, location=location, page_token=places_result['next_page_token'])
        else:
            break

# Start fetching
print("Fetching companies from Indiana...")
fetch_places(SEARCH_QUERY, LOCATION)

# Save Excel file
wb.save("indiana_companies.xlsx")
print("Data saved to indiana_companies.xlsx")