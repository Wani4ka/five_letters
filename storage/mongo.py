import logging

import bson.errors
from bson import ObjectId
from pymongo import MongoClient

from game.room import Room
from storage import BaseStorage, RoomNotFoundError
from words import words

LOGGER = logging.getLogger(__name__)

class MongoStorage(BaseStorage):
    def __init__(self, db_name: str, url: str):
        self.client = MongoClient(url)
        conn = self.client[db_name]

        collections = conn.list_collection_names()
        if "words" not in collections:
            LOGGER.info('Initializing collection "words" with default words list')
            conn["words"].insert_many(map(lambda word: {'value': word}, words))

        self.words_collection = conn["words"]
        self.rooms_collection = conn["rooms"]

    def __del__(self):
        self.client.close()

    def random_word(self) -> str:
        aggr = list(self.words_collection.aggregate([{ "$sample": {"size": 1}}]))
        return aggr[0]['value']

    def save_room(self, room: Room):
        room.room_id = str(self.rooms_collection.insert_one({
            'word': room.word,
            'attempts': room.attempts,
        }).inserted_id)

    def get_room(self, room_id: str) -> Room:
        try:
            object_id = ObjectId(room_id)
        except bson.errors.InvalidId:
            raise RoomNotFoundError from None
        doc = self.rooms_collection.find_one({"_id": object_id})
        if doc is None:
            raise RoomNotFoundError
        return Room(
            room_id=doc['_id'],
            word=doc['word'],
            attempts=doc['attempts'],
        )

    def update_room(self, room: Room):
        self.rooms_collection.update_one(
            {"_id": ObjectId(room.room_id)},
            {
                "$set": {
                    "word": room.word,
                    "attempts": room.attempts,
                }
            }
        )

    def delete_room(self, room_id: str) -> None:
        self.rooms_collection.delete_one({"_id": ObjectId(room_id)})
