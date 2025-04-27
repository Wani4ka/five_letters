# main.py
from game.game import Game

if __name__ == '__main__':
    game = Game()
    room = game.create_room()
    print(f"Создана комната с id {room.room_id}. Угадайте слово!")

    while True:
        guess = input("Введите слово: ")
        try:
            response, finished, solution = game.try_guess(room.room_id, guess)
        except Exception as e:
            print(str(e))
        else:
            print("Подсказки:", response)
            if finished:
                print("Игра окончена!")
                print(f"Слово было: {solution}")
                break
