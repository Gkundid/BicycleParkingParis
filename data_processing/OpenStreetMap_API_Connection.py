import requests
import csv

def fetch_osm_data():
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = """
    [out:json][timeout:25];
    // Définition de la zone géographique de Paris
    (area["name"="Paris"]["boundary"="administrative"];)->.searchArea;
    (
      node["amenity"="bicycle_parking"](area.searchArea);
      way["amenity"="bicycle_parking"](area.searchArea);
      relation["amenity"="bicycle_parking"](area.searchArea);
    );
    out body;
    >;
    out skel qt;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()
    return data['elements']

def save_to_csv(elements, filename='bicycle_parking_paris.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Labels', 'Latitude', 'Longitude', 'Capacity'])
        
        parking_count = 1
        for element in elements:
            lat = element.get('lat')
            lon = element.get('lon')
            capacity = element.get('tags', {}).get('capacity')  # Cherche le champ 'capacity' dans les tags
            name = "ParkingVelo"
            parking_count += 1
            if lat and lon and capacity:  # Vérifie si tous les champs nécessaires sont présents
                writer.writerow([name, lat, lon, capacity])

if __name__ == '__main__':
    elements = fetch_osm_data()
    save_to_csv(elements)
