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

def save_to_csv(elements, filename='parkings_a_velo_paris.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Latitude', 'Longitude'])

        for element in elements:
            lat = element.get('lat')
            lon = element.get('lon')
            name = element.get('tags', {}).get('name', 'Unknown')
            if lat and lon:
                writer.writerow([name, lat, lon])

if __name__ == '__main__':
    elements = fetch_osm_data()
    save_to_csv(elements)