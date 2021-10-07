import os
from dotenv import load_dotenv
import pymongo

load_dotenv()

client = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("TESTDB")]


def user_register(
    user_name: str = "Test",
    email: str = "tester@example.com",
    password: str = "password",
    units: int = 10,
):
    doc = {
        "user_name": user_name,
        "email": email,
        "password": password,
        "units": units,
    }

    return doc


def clear_all():
    db.drop_collection("users")
    db.drop_collection("units")


DATABASE = {
    "Production": {
        "MONGO_URI": os.getenv("MONGO_URI"),
        "DB": os.getenv("DB"),
    },
    "Test": {"MONGO_URI": os.getenv("MONGO_URI"), "DB": os.getenv("TESTDB")},
}
