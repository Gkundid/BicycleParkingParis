from flask import Flask, request, jsonify
import os
import dotenv
from neo4j import GraphDatabase

app = Flask(__name__)

# Get current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Complete path directory for file configuration
config_file_path = os.path.join(current_directory, "Credentials-Neo4j-Instance.txt")

# Chargez les variables d'environnement à partir du fichier de configuration
load_status = dotenv.load_dotenv(config_file_path)
if load_status is False:
    raise RuntimeError('Environment variables not loaded.')

# Obtenez les variables d'environnement nécessaires pour la connexion
URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

# Classe pour gérer la connexion Neo4j
class Neo4jConnection:
    def __init__(self):
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(URI, auth=AUTH)
            self.__driver.verify_connectivity()
            print("Successful Connection to Database!")
        except Exception as e:
            print(f"Failed to create the driver: {e}")
    
    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def execute_query(self, query, parameters=None, db=None):
        with self.__driver.session(database=db) as session:
            result = session.run(query, parameters)
            return [record for record in result]

neo4j_conn = Neo4jConnection()

@app.route('/api/parking/search', methods=['GET'])
def search_parking():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    
    # Exemple de requête Cypher, à remplacer par votre requête spécifique
    query = """
    MATCH (p:Parking) WHERE distance(p.location, point({latitude: $lat, longitude: $lon})) < 1000
    RETURN p ORDER BY distance(p.location, point({latitude: $lat, longitude: $lon})) ASC LIMIT 5
    """
    try:
        results = neo4j_conn.execute_query(query, parameters={'lat': lat, 'lon': lon})
        return jsonify([{"lat": record["p"]["latitude"], "lon": record["p"]["longitude"]} for record in results])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
