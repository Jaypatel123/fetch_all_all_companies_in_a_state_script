import os
import googlemaps
import time
import csv
from dotenv import load_dotenv
load_dotenv()
# Initialize Google Maps client
API_KEY = os.getenv('API_KEY')
print(API_KEY)
gmaps = googlemaps.Client(key=API_KEY)

# Sample list of Indiana cities — can be expanded
indiana_places = [
    # Cities (117 is the official count, this list is extensive but may not be exhaustive of *all* 117 cities,
    # as some are very small and less commonly listed individually.)
    "Anderson",
    "Angola",
    "Attica",
    # "Auburn",
    # "Aurora",
    # "Austin",
    # "Batesville",
    # "Bedford",
    # "Beech Grove",
    # "Berne",
    # "Bicknell",
    # "Bluffton",
    # "Bloomington",
    # "Boonville",
    # "Brazil",
    # "Butler",
    # "Carmel",
    # "Charlestown",
    # "Clinton",
    # "Columbia City",
    # "Columbus",
    # "Connersville",
    # "Crawfordsville",
    # "Crown Point",
    # "Decatur",
    # "Delphi",
    # "Dunkirk",
    # "East Chicago",
    # "Elkhart",
    # "Elwood",
    # "Evansville",
    # "Fort Wayne",
    # "Frankfort",
    # "Franklin",
    # "Garrett",
    # "Gary",
    # "Gas City",
    # "Goshen",
    # "Greencastle",
    # "Greenfield",
    # "Greensburg",
    # "Greenwood",
    # "Hammond",
    # "Hartford City",
    # "Hobart",
    # "Huntingburg",
    # "Huntington",
    # "Indianapolis",  # Note: Indianapolis is a consolidated city-county (Marion County)
    # "Jasonville",
    # "Jasper",
    # "Jeffersonville",
    # "Kendallville",
    # "Knox",
    # "Kokomo",
    # "Lafayette",
    # "Lake Station",
    # "Lawrence",
    # "Lawrenceburg",
    # "Lebanon",
    # "Ligonier",
    # "Linton",
    # "Logansport",
    # "Madison",
    # "Marion",
    # "Martinsville",
    # "Michigan City",
    # "Mishawaka",
    # "Mitchell",
    # "Monticello",
    # "Mount Vernon",
    # "Muncie",
    # "Nappanee",
    # "New Albany",
    # "New Castle",
    # "New Haven",
    # "Noblesville",
    # "North Vernon",
    # "Oakland City",
    # "Oldenburg",
    # "Paoli",
    # "Peru",
    # "Petersburg",
    # "Plymouth",
    # "Portage",
    # "Portland",
    # "Princeton",
    # "Rensselaer",
    # "Richmond",
    # "Rising Sun",
    # "Rochester",
    # "Rockport",
    # "Rushville",
    # "Salem",
    # "Scottsburg",
    # "Seymour",
    # "Shelbyville",
    # "South Bend",
    # "Southport",
    # "Sullivan",
    # "Tell City",
    # "Terre Haute",
    # "Tipton",
    # "Valparaiso",
    # "Vincennes",
    # "Wabash",
    # "Warsaw",
    # "Washington",
    # "West Lafayette",
    # "Westfield",
    # "Whiting",
    # "Winchester",
    # "Woodburn",
    # "Zionsville",
    # # Major Towns (These are often among the largest towns by population)
    # "Avon",
    # "Bargersville",
    # "Brownsburg",
    # "Chesterton",
    # "Clarksville",
    # "Dyer",
    # "Fishers", # Note: Fishers became a city in 2015, but is often still thought of as a large town. Included here for comprehensive "big town" representation.
    # "Fortville",
    # "Greenwood", # Note: Greenwood is a city, but due to its size and growth, it's often associated with the 'large suburban town' feel. Already in cities.
    # "Merrillville",
    # "Mooresville",
    # "Munster",
    # "Plainfield",
    # "Schererville",
    # "Sellersburg",
    # "St. John",
    # "Speedway",
    # "Winamac",
    # "Whitestown",
    # "Whiteland",
]


# Broad search keywords
search_keywords = ["company", "office"]

# Results list and set of seen place_ids
all_results = []
seen_place_ids = set()

for city in indiana_places:
    for keyword in search_keywords:
        print(f"🔍 Searching '{keyword}' in indiana...")

        try:
            # Perform Places API search
            response = gmaps.places(
                query=keyword,
                location=f"Indiana",
                radius=200000
            )

            places = response.get("results", [])

            for place in places:
                place_id = place.get("place_id")

                # Skip duplicates
                if place_id in seen_place_ids:
                    continue
                seen_place_ids.add(place_id)

                name = place.get("name")
                address = place.get("formatted_address", "N/A")
                types = ", ".join(place.get("types", []))
                rating = place.get("rating", "N/A")
                business_status = place.get("business_status", "N/A")

                # Fetch detailed info
                try:
                    details = gmaps.place(place_id=place_id).get("result", {})
                    phone = details.get("formatted_phone_number", "N/A")
                    website = details.get("website", "N/A")
                except Exception as e:
                    print(f"⚠️ Details fetch failed for {name}: {str(e)}")
                    phone = "N/A"
                    website = "N/A"

                all_results.append({
                    "city": city,
                    "keyword": keyword,
                    "name": name,
                    "address": address,
                    "phone": phone,
                    "website": website,
                    "rating": rating,
                    "business_status": business_status,
                    "types": types
                })

                time.sleep(4)  # Delay to avoid throttling

            time.sleep(10)  # Delay between search requests
        except Exception as e:
            print(f"❌ Error in {city} - '{keyword}': {str(e)}")

# Write unique businesses to CSV
if all_results:
    with open("indiana_unique_businesses.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_results[0].keys())
        writer.writeheader()
        writer.writerows(all_results)
    print(f"✅ Done. {len(all_results)} unique businesses saved to 'indiana_unique_businesses.csv'")
else:
    print("⚠️ No businesses found.")
