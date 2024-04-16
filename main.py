from fastapi import FastAPI
from api.question_answering import router
from pymongo.mongo_client import MongoClient

app = FastAPI()

# Create a new client and connect to the server
uri = "mongodb://localhost:27017/"
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app.include_router(router)