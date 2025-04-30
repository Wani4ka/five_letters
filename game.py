from random import choice

from words import words

max_attempts = 6
next_room_id = 1
rooms = {}


def create_room():
    global next_room_id
    room_id = next_room_id
    next_room_id += 1
    rooms[room_id] = (choice(words), 0)
    return room_id


def try_guess(room_id, guess):
    if len(guess) != 5:
        raise Exception('word should be 5 characters long')
    guess = guess.upper()

    if room_id not in rooms:
        raise Exception('room not found')
    word, attempts = rooms[room_id]
    attempts += 1
    room_removed = False

    if attempts == max_attempts:
        del rooms[room_id]
        room_removed = True
    else:
        rooms[room_id] = (word, attempts)

    response = [0, 0, 0, 0, 0]  # 0 = серый, 1 = желтый, 2 = зеленый
    for i in range(len(response)):
        if guess[i] in word:
            response[i] = 1
        if guess[i] == word[i]:
            response[i] = 2

    if guess == word:
        del rooms[room_id]
        room_removed = True

    return response, room_removed
