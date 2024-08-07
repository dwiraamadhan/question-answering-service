from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGODB_URL"))
db = client["audio_ml"]
collection = db ["question"]