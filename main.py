import game

if __name__ == '__main__':
    roomID = game.create_room()

    while True:
        guess = input()
        try:
            response, removed = game.try_guess(roomID, guess)
        except Exception as e:
            print(str(e))
        else:
            print(response)
            if removed:
                break
