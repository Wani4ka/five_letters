from random import choice

from words import words

# Множество допустимых русских букв (в верхнем регистре)
RUSSIAN_LETTERS = set("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")


class Room:
    max_attempts = 6

    def __init__(self, room_id: int):
        self.room_id = room_id
        self.word = choice(words)
        self.attempts = Room.max_attempts

    def try_guess(self, guess: str) -> list:
        if len(guess) != 5:
            raise ValueError("Предложенное слово состоит не из пяти символов")

        if not all(ch.upper() in RUSSIAN_LETTERS for ch in guess):
            raise ValueError(
                "Предложенное слово содержит иные символы, кроме букв русского алфавита"
            )

        guess = guess.upper()
        self.attempts -= 1

        response = [0] * 5
        for i in range(5):
            if guess[i] == self.word[i]:
                response[i] = 2
        for i in range(5):
            if response[i] == 0 and guess[i] in self.word:
                response[i] = 1

        return response

    def is_finished(self, guess: str) -> bool:
        return guess.upper() == self.word or self.attempts <= 0
