from flask import Flask, request, jsonify
import os
import dotenv
from neo4j import GraphDatabase
from flask_cors import CORS
 
app = Flask(__name__)
CORS(app)

# Get current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Complete path directory for file configuration
config_file_path = os.path.join(current_directory, "Credentials-Neo4j-Instance.txt")

# Load environment variables from the configuration file
load_status = dotenv.load_dotenv(config_file_path)
if load_status is False:
    raise RuntimeError('Environment variables not loaded.')

# Get the necessary environment variables for connection
URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

# Class to manage Neo4j connection
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
    
    # Updated Cypher query with type conversion
    query = """
    MATCH (p:ParkingVelo)
    WHERE point.distance(point({latitude: toFloat(p.Latitude), longitude: toFloat(p.Longitude)}), point({latitude: $lat, longitude: $lon})) < 1000
    RETURN p.ID, p.Latitude, p.Longitude, p.Capacity
    ORDER BY point.distance(point({latitude: toFloat(p.Latitude), longitude: toFloat(p.Longitude)}), point({latitude: $lat, longitude: $lon})) ASC
    LIMIT 5
    """
    try:
        results = neo4j_conn.execute_query(query, parameters={'lat': lat, 'lon': lon})
        # Adjusting the return statement to match the structure of the results
        print(results)
        return jsonify([{"id": record["p.ID"], "lat": record["p.Latitude"], "lon": record["p.Longitude"], "capacity": record["p.Capacity"]} for record in results])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)