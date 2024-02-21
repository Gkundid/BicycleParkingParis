import requests
import csv
import time

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

def reverse_geocode(lat, lon):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
        response = requests.get(url, timeout=1.5)  # Définir un timeout de 10 secondes
        data = response.json()
        return data.get("display_name", "Adresse non trouvée")
    except requests.exceptions.RequestException as e:
        print(f"Erreur de requête pour {lat}, {lon}: {e}")
        return "Erreur de requête"
    finally:
        time.sleep(1)  # Attendre 1 seconde entre les requêtes

def add_addresses_to_csv(input_filename, output_filename):
    with open(input_filename, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_filename, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['Address']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            address = reverse_geocode(row['Latitude'], row['Longitude'])
            row['Address'] = address
            writer.writerow(row)

if __name__ == '__main__':
    elements = fetch_osm_data()
    save_to_csv(elements)
    input_csv_filename = 'parkings_a_velo_paris.csv'
    output_csv_filename = 'parkings_a_velo_paris_with_addresses.csv'
    add_addresses_to_csv(input_csv_filename, output_csv_filename)