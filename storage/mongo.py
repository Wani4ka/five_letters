from pymongo import MongoClient

from game.room import Room
from storage import BaseStorage, RoomNotFoundError


class MongoStorage(BaseStorage):
    def __init__(self, db_name: str, url: str):
        self.client = MongoClient(url)
        conn = self.client[db_name]

        collections = conn.list_collection_names()
        if "words" not in collections:
            raise Exception('Please initialize "words" collection first')
        self.words_collection = conn["words"]
        self.rooms_collection = conn["rooms"]

    def __del__(self):
        self.client.close()

    def random_word(self) -> str:
        return list(self.words_collection.aggregate([{ "$sample": {"size": 1}}]))[0].value

    def save_room(self, room: Room):
        room.room_id = self.rooms_collection.insert_one({
            'word': room.word,
            'attempts': room.attempts,
        }).inserted_id

    def get_room(self, room_id: str) -> Room:
        doc = self.rooms_collection.find_one({"_id": room_id})
        if doc is None:
            raise RoomNotFoundError
        return Room(
            room_id=doc['_id'],
            word=doc['word'],
            attempts=doc['attempts'],
        )

    def delete_room(self, room_id: str) -> None:
        self.rooms_collection.delete_one({"_id": room_id})
