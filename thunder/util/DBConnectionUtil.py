from pymongo import MongoClient


def get_connection():
    """
    This create a mongodb connection and return the collection that we use in this project
    The database we are using in this project named "Olympians"
    And we are using "Parthenon"
    """
    try:
        client = MongoClient("mongodb://root:root@mongo:27017/")
        # If need local debug replace the ip to router ip
        # client = MongoClient("mongodb://root:root@192.168.50.113:27017/")
        db = client["Olympians"]
        col = db["Parthenon"]

        return col
    except Exception as e:
        print(f"Unable to connect to the server. {e}")
