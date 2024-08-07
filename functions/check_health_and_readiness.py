from confluent_kafka import Producer, KafkaError
import socket, os
from pymongo.mongo_client import MongoClient

def check_kafka_connection():
    try:
        # kafka configuration
        conf = {
            "bootstrap.servers" : os.getenv("BROKER_SERVER"),
            "client.id" : socket.gethostname(),
        }

        # check connection kafka with getting list of topics
        producer = Producer(conf)
        producer.list_topics()
        print("Successfully connected to Kafka using Producer!")

        return True

    except Exception as e:
        print(f"Failed to connect to Kafka server: {e}")
        return False



# check connection to mongo db
def check_db_connection():
    # Create a new client and connect to the server
    uri = os.getenv("MONGODB_URL")
    client = MongoClient(uri)


    # Send a ping to confirm a successful connection
    try:
        client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return True
    
    except Exception as e:
        print(e)
        return False
    
