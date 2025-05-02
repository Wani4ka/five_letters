from game.room import Room


class Game:
    def __init__(self):
        self.next_room_id = 1
        self.rooms = {}

    def create_room(self) -> Room:
        room = Room(self.next_room_id)
        self.rooms[self.next_room_id] = room
        self.next_room_id += 1
        return room

    def try_guess(self, room_id: int, guess: str) -> tuple[list, bool, str | None]:
        if room_id not in self.rooms:
            raise Exception("Комната не найдена")
        room = self.rooms[room_id]
        response = room.try_guess(guess)
        finished = room.is_finished(guess)

        solution = None
        if finished:
            solution = room.word
            del self.rooms[room_id]
        return response, finished, solution
