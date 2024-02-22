import os
import csv
import dotenv
from neo4j import GraphDatabase

# Get current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Complete path directory for file configuration
config_file_path = os.path.join(current_directory, "Credentials-Neo4j-Instance.txt")

csv_file_path = os.path.join(current_directory, "bicycle_parking_paris.csv")

def Create_nodes(csv_file_path):    
    try:
        with open(csv_file_path, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for index, row in enumerate(reader, start=1):
                    properties = {key: value for key, value in row.items()}
                    properties["ID"] = index

                    properties_str = "{" + ", ".join([f"{key}: '{value}'" for key, value in properties.items()]) + "}"
                    query = f"MERGE (p:ParkingVelo {properties_str})"

                    summary = driver.execute_query(query, database_="neo4j").summary

                    print("Created {nodes_created} nodes in {time} ms.".format(
                        nodes_created=summary.counters.nodes_created,
                        time=summary.result_available_after
                    ))
    except Exception as e:
        print(e)
        # further logging/processing


load_status = dotenv.load_dotenv(config_file_path)
if load_status is False:
    raise RuntimeError('Environment variables not loaded.')

URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    print("Successfull Connection to Database !")
    Create_nodes(csv_file_path)
