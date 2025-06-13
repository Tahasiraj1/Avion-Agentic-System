from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGODB_URI)

class DB:
    def __init__(self):
        # Accessing the DB
        self.db = client['CustomerOrders']
    