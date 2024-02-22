import os
import csv
import dotenv
from neo4j import GraphDatabase

# Get current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Complete path directory for file configuration
config_file_path = os.path.join(current_directory, "Credentials-Neo4j-Instance.txt")

# Chemin absolu du fichier CSV dans le même répertoire que Write_database.py
csv_file_path = os.path.join(current_directory, "bicycle_parking_paris.csv")

def Create_nodes(csv_file_path):    
    try:
        # Lecture du fichier CSV
        with open(csv_file_path, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                # Parcours des lignes du fichier CSV
                for row in reader:
                    # Extraction des libellés et des propriétés
                    labels = row["Labels"]
                    properties = {key: value for key, value in row.items() if key != "Labels"}

                    # Construction de la requête Cypher avec les propriétés correctement formatées
                    properties_str = "{" + ", ".join([f"{key}: '{value}'" for key, value in properties.items()]) + "}"
                    query = f"MERGE (p:{labels} {properties_str})"

                    # Exécution de la requête Cypher
                    summary = driver.execute_query(query, database_="neo4j").summary

                    print("Created {nodes_created} nodes in {time} ms.".format(
                        nodes_created=summary.counters.nodes_created,
                        time=summary.result_available_after
                    ))
    except Exception as e:
        print(e)
        # further logging/processing


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
    Create_nodes(csv_file_path)
    # Fermez explicitement la connexion après avoir terminé
    # driver.close()