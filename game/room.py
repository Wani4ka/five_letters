from random import choice
from words import words

class Room:
    max_attempts = 6

    def __init__(self, room_id: int):
        self.room_id = room_id
        self.word = choice(words)
        self.attempts = 0

    def try_guess(self, guess: str) -> list:
        if len(guess) != 5:
            raise Exception('Слово должно состоять из 5 символов')
        
        guess = guess.upper()
        self.attempts += 1

        response = [0] * 5
        for i in range(5):
            if guess[i] == self.word[i]:
                response[i] = 2
        for i in range(5):
            if response[i] == 0 and guess[i] in self.word:
                response[i] = 1

        return response

    def is_finished(self, guess: str) -> bool:
        return guess.upper() == self.word or self.attempts >= Room.max_attempts
