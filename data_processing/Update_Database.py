import os
import dotenv
from neo4j import GraphDatabase

# Get current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Complete path directory for file configuration
config_file_path = os.path.join(current_directory, "Credentials-Neo4j-Instance.txt")

def Update_Database():
    records, summary, keys = driver.execute_query("""
        MATCH (p:ParkingVelo1 {Gratuit: $Gratuit})
        SET p.Capacite = $Capacite
        """, Gratuit="true", Capacite=42,
        database_="neo4j",
    )
    print(f"Query counters: {summary.counters}.")

# Chargez les variables d'environnement à partir du fichier de configuration
load_status = dotenv.load_dotenv(config_file_path)
if load_status is False:
    raise RuntimeError('Environment variables not loaded.')

# Obtenez les variables d'environnement nécessaires pour la connexion
URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

# Connectez-vous à la base de données Neo4j
with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    print("Successfull Connection to Database !")




