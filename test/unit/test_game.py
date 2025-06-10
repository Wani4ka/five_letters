from game.game import Game
from game.room import Room


def test_create_room():
    """Проверка создания комнаты."""
    game = Game()
    room = game.create_room()
    assert isinstance(room, Room), "Должен возвращаться объект Room"
    assert game.next_room_id == 2, "ID следующей комнаты должен увеличиться"
    assert len(game.rooms) == 1, "Комната должна добавляться в словарь комнат"


def test_try_guess_correct():
    """Проверка правильной догадки."""
    game = Game()
    room = game.create_room()
    room.word = "ПЯТКА"

    response, finished, solution = game.try_guess(room.room_id, "пятка")
    assert response == [2, 2, 2, 2, 2], "Некорректный ответ для правильной догадки"
    assert finished, "Игра должна завершиться"
    assert solution == "ПЯТКА", "Должно возвращаться загаданное слово"
    assert room.room_id not in game.rooms, "Комната должна удаляться после завершения"


def test_try_guess_wrong_room():
    """Проверка обработки несуществующей комнаты."""
    game = Game()
    try:
        game.try_guess(999, "apple")
        raise AssertionError("Ожидалось исключение для несуществующей комнаты")
    except Exception as e:
        assert str(e) == "Комната не найдена", "Некорректное сообщение об ошибке"


def test_multiple_rooms():
    """Проверка работы с несколькими комнатами."""
    game = Game()
    room1 = game.create_room()
    room2 = game.create_room()

    assert room1.room_id == 1, "Некорректный ID первой комнаты"
    assert room2.room_id == 2, "Некорректный ID второй комнаты"
    assert len(game.rooms) == 2, "Должны создаваться несколько комнат"
