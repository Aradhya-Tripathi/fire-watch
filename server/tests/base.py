import os
from dotenv import load_dotenv

load_dotenv()


def school_register(
    school_name: str = "Test",
    email: str = "tester@example.com",
    password: str = "password",
    units: int = 10,
):
    doc = {
        "school_name": school_name,
        "email": email,
        "password": password,
        "units": units,
    }

    return doc


DATABASE = {
    "Production": {
        "MONGO_URI": os.getenv("MONGO_URI"),
        "DB": os.getenv("DB"),
    },
    "Test": {"MONGO_URI": os.getenv("MONGO_URI"), "DB": os.getenv("TESTDB")},
}
