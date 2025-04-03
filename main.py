import game

if __name__ == '__main__':
    room_id = game.create_room()

    while True:
        guess = input()
        try:
            response, removed = game.try_guess(room_id, guess)
        except Exception as e:
            print(str(e))
        else:
            print(response)
            if removed:
                break
