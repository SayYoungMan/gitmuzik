from datetime import datetime, timedelta
import logging
import os

from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from music import MusicMetaData

DATABASE_NAME = "daily_playlist"

def get_mongo_client() -> MongoClient:
    uri = os.environ["MONGO_DB_URI"]
    return MongoClient(uri, server_api=ServerApi('1'))

def _get_mongo_db(client: MongoClient) -> Database:
    return client[DATABASE_NAME]

def _get_last_collection(db: Database) -> Collection:
    collection_names = db.list_collection_names()
    latest_collection_name = max(collection_names)

    return db.get_collection(latest_collection_name)

def _create_collection(db: Database, collection_name: str) -> Collection:
    return db.create_collection(collection_name)

def _write_music_documents(collection: Collection, music_data: list[MusicMetaData]):
    documents = [ data.to_dict() for data in music_data ]
    res = collection.insert_many(documents)
    
    if not res.acknowledged:
        logging.error("Bulk insert of music documents failed.")
        return
    
    logging.info("Successfully inserted music data to %s.", collection.name)

def write_music_data_to_db(client: MongoClient, music_data: list[MusicMetaData]):
    db = _get_mongo_db(client)

    # Create a collection with name of today's date
    today = datetime.today().strftime('%Y-%m-%d')
    collection = _create_collection(db, today)

    _write_music_documents(collection, music_data)

def get_last_music_titles(client: MongoClient) -> dict[str, bool]:
    db = _get_mongo_db(client)
    last_collection = _get_last_collection(db)
    last_music_data = list(last_collection.find())

    res = {}
    for data in last_music_data:
        res[data["title"]] = True

    return res
