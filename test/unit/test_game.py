from game.game import Game
from game.room import Room
from storage.in_memory import InMemoryStorage
from words import words


def test_create_room():
    """Проверка создания комнаты."""
    storage = InMemoryStorage(words)
    game = Game(storage)
    room = game.create_room()
    assert isinstance(room, Room), "Должен возвращаться объект Room"
    assert room.room_id is not None, "ID комнаты должен быть установлен"
    assert len(storage.rooms) == 1, "Комната должна добавляться в словарь комнат"


def test_try_guess_correct():
    """Проверка правильной догадки."""
    storage = InMemoryStorage(words)
    game = Game(storage)
    room = game.create_room()
    room.word = "ПЯТКА"

    response, finished, attempts, solution = game.try_guess(room.room_id, "пятка")
    assert response == [2, 2, 2, 2, 2], "Некорректный ответ для правильной догадки"
    assert finished, "Игра должна завершиться"
    assert solution == "ПЯТКА", "Должно возвращаться загаданное слово"
    assert room.room_id not in storage.rooms, "Комната должна удаляться после завершения"


def test_try_guess_wrong_room():
    """Проверка обработки несуществующей комнаты."""
    storage = InMemoryStorage(words)
    game = Game(storage)
    try:
        game.try_guess("invalid_room_id", "apple")
        raise AssertionError("Ожидалось исключение для несуществующей комнаты")
    except KeyError as e:
        assert (str(e).strip("'") ==
                "Комната с таким идентификатором не существует или игра в ней была завершена"),\
            "Некорректное сообщение об ошибке"
    except Exception as e:
        raise AssertionError("Ожидалось исключение KeyError") from e


def test_multiple_rooms():
    """Проверка работы с несколькими комнатами."""
    storage = InMemoryStorage(words)
    game = Game(storage)
    room1 = game.create_room()
    room2 = game.create_room()

    assert room1 is not None, "Некорректный ID первой комнаты"
    assert room2 is not None, "Некорректный ID второй комнаты"
    assert room1.room_id != room2.room_id, "ID комнат не отличаются"
    assert len(storage.rooms) == 2, "Должны создаваться несколько комнат"
