from game.room import Room


def test_try_guess_correct():
    """Проверка правильной догадки."""
    room = Room(room_id=1)
    room.word = "APPLE"
    response = room.try_guess("apple")
    assert response == [2, 2, 2, 2, 2], "Некорректный ответ для полного совпадения"
    assert room.attempts == 1, "Счетчик попыток должен увеличиться"


def test_try_guess_wrong_length():
    """Проверка обработки неправильной длины слова."""
    room = Room(room_id=1)
    try:
        room.try_guess("app")
        raise AssertionError("Ожидалось исключение для неправильной длины")
    except Exception as e:
        assert str(e) == "Слово должно состоять из 5 символов", "Некорректное сообщение об ошибке"


def test_try_guess_partial_match():
    """Проверка частичного совпадения."""
    room = Room(room_id=1)
    room.word = "APPLE"
    response = room.try_guess("apxle")
    assert response == [2, 2, 0, 2, 2], "Некорректный ответ для частичного совпадения"


def test_is_finished_correct_guess():
    """Проверка завершения игры при правильной догадке."""
    room = Room(room_id=1)
    room.word = "APPLE"
    assert room.is_finished("apple"), "Игра должна завершиться при правильном ответе"


def test_is_finished_max_attempts():
    """Проверка завершения игры при максимальном числе попыток."""
    room = Room(room_id=1)
    room.attempts = Room.max_attempts
    assert room.is_finished("xxxxx"), "Игра должна завершиться при max_attempts"


def test_try_guess_letter_in_word():
    """Проверка случая, когда буква есть в слове, но на другой позиции."""
    room = Room(room_id=1)
    room.word = "APPLE"
    response = room.try_guess("peach")  # Буква 'P' есть в 'APPLE', но на другой позиции
    assert response == [1, 1, 1, 0, 0], "Некорректный ответ для буквы в слове, но не на позиции"
    assert room.attempts == 1, "Счетчик попыток должен увеличиться"
