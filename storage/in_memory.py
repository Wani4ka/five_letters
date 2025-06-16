from random import choice
from secrets import token_hex

from game.room import Room
from storage import BaseStorage, RoomNotFoundError


class InMemoryStorage(BaseStorage):
    def __init__(self, words: list):
        self.words = words
        self.rooms = {}

    def random_word(self) -> str:
        return choice(self.words)

    def save_room(self, room: Room):
        room_id = token_hex()
        self.rooms[room_id] = room
        room.room_id = room_id

    def get_room(self, room_id: str) -> Room:
        if room_id not in self.rooms:
            raise RoomNotFoundError

        return self.rooms[room_id]

    def update_room(self, room: Room):
        pass

    def delete_room(self, room_id: str) -> None:
        if room_id in self.rooms:
            del self.rooms[room_id]
