import os
import dotenv
from neo4j import GraphDatabase

# Get current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Complete path directory for file configuration
config_file_path = os.path.join(current_directory, "Credentials-Neo4j-Instance.txt")


def Read_From_Database():    
    records, summary, keys = driver.execute_query(
        "MATCH (p:ParkingVelo1) MATCH (gq:ParkingVelo2) RETURN p.Capacite AS Capacite, gq.Longitude AS Longitude ", #Requête de lecture pour deux noeuds différents
        database_="neo4j",
    )

    # Loop through results and do something with them
    for record in records:
        print(record.data())  # obtain record as dict

    # Summary information
    print("The query `{query}` returned {records_count} records in {time} ms.".format(
        query=summary.query, records_count=len(records),
        time=summary.result_available_after
    ))

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

    Read_From_Database()

    
    
    
