import json

# Load the GeoJSON file with UTF-8 encoding
try:
    with open(r"C:\Users\Franko\Desktop\Fakultet\4. godina\8. semestar\Vizualizacija podataka\DataVisualizationProject\geojson\custom.geo.json", "r", encoding="utf-8") as f:
        geo_data = json.load(f)
except UnicodeDecodeError as e:
    print(f"Error: Failed to decode the file with UTF-8 encoding: {e}")
    print("The file may be encoded in a different format. Try opening it in a text editor to check its encoding.")
    exit(1)
except json.JSONDecodeError as e:
    print(f"Error: The file is not a valid JSON: {e}")
    print("Please verify the GeoJSON file is correctly formatted.")
    exit(1)
except FileNotFoundError:
    print("Error: custom.geo.json not found at the specified path.")
    exit(1)

# Function to check if a polygon is likely French Guiana
def is_french_guiana(polygon):
    # French Guiana is in South America, roughly between lon: -54 to -51, lat: 2 to 6
    for ring in polygon:
        for lon, lat in ring:
            if -54 <= lon <= -51 and 2 <= lat <= 6:
                return True
    return False

# Find France's feature
found = False
for feature in geo_data["features"]:
    if feature["properties"].get("name") == "France" or feature["properties"].get("adm0_a3") == "FRA":
        found = True
        # France's geometry is a MultiPolygon
        if feature["geometry"]["type"] == "MultiPolygon":
            # Filter out polygons that match French Guiana's coordinates
            feature["geometry"]["coordinates"] = [
                polygon for polygon in feature["geometry"]["coordinates"]
                if not is_french_guiana(polygon)
            ]
            # If the MultiPolygon is empty, convert to Polygon or handle as needed
            if len(feature["geometry"]["coordinates"]) == 1:
                feature["geometry"]["type"] = "Polygon"
                feature["geometry"]["coordinates"] = feature["geometry"]["coordinates"][0]
        break

if not found:
    print("Warning: France not found in GeoJSON. Please verify the feature exists.")

# Save the modified GeoJSON with UTF-8 encoding
with open(r"C:\Users\Franko\Desktop\Fakultet\4. godina\8. semestar\Vizualizacija podataka\DataVisualizationProject\geojson\custom_no_guiana.geo.json", "w", encoding="utf-8") as f:
    json.dump(geo_data, f, indent=2)

print("Updated GeoJSON saved as 'custom_no_guiana.geo.json'")