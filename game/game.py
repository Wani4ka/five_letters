import storage
from game.room import Room


class Game:
    def __init__(self, store: storage.BaseStorage):
        self.rooms = {}
        self.store = store

    def create_room(self) -> Room:
        room = Room(self.store.random_word())
        self.store.save_room(room)
        return room

    def try_guess(self, room_id: str, guess: str) -> tuple[list, bool, int, str | None]:
        room = self.store.get_room(room_id)
        response = room.try_guess(guess)
        finished = room.is_finished(guess)

        solution = None
        if finished:
            solution = room.word
            del self.rooms[room_id]
        return response, finished, room.attempts, solution
