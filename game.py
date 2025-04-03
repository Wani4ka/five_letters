from words import words
from random import choice

max_attempts = 6
next_room_id = 1
rooms = {}

def create_room():
    global next_room_id
    roomID = next_room_id
    next_room_id += 1
    rooms[roomID] = (choice(words), 0)
    return roomID

def try_guess(roomID, guess):
    if len(guess) != 5:
        raise Exception('word should be 5 characters long')
    guess = guess.upper()

    if not roomID in rooms:
        raise Exception('room not found')
    word, attempts = rooms[roomID]
    attempts += 1
    room_removed = False

    if attempts == max_attempts:
        del(rooms[roomID])
        room_removed = True
    else:
        rooms[roomID] = (word, attempts)

    response = [0, 0, 0, 0, 0] # 0 = серый, 1 = желтый, 2 = зеленый
    for i in range(len(response)):
        if guess[i] in word:
            response[i] = 1
        if guess[i] == word[i]:
            response[i] = 2

    if guess == word:
        del(rooms[roomID])
        room_removed = True

    return response, room_removed
