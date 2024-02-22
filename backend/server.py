from flask import Flask, request, jsonify
import os
import dotenv
from neo4j import GraphDatabase

app = Flask(__name__)

# Chemin vers le fichier de configuration pour les credentials Neo4j
dotenv_path = os.path.join(os.path.dirname(__file__), 'Credentials-Neo4j-Instance.txt')
dotenv.load_dotenv(dotenv_path)

# Paramètres de connexion Neo4j
URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

# Classe pour gérer la connexion Neo4j
class Neo4jConnection:
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
            self.__driver.verify_connectivity()
            print("Connected to Neo4j")
        except Exception as e:
            print("Failed to create the driver:", e)
        
    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def execute_query(self, query, parameters=None, db=None):
        with self.__driver.session(database=db) as session:
            result = session.run(query, parameters)
            return [record for record in result]

# Création de l'instance de connexion
neo4j_conn = Neo4jConnection(URI, USERNAME, PASSWORD)

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
