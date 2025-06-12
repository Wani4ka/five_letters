from game.room import Room


def test_try_guess_correct():
    """Проверка правильной догадки."""
    room = Room(room_id=1)
    room.word = "ПЯТКА"
    attempts = room.attempts
    response = room.try_guess("пятка")
    assert response == [2, 2, 2, 2, 2], "Некорректный ответ для полного совпадения"
    assert room.attempts == attempts - 1, "Счетчик оставшихся попыток должен уменьшиться"


def test_try_guess_wrong_length():
    """Проверка обработки неправильной длины слова."""
    room = Room(room_id=1)
    try:
        room.try_guess("пят")
        raise AssertionError("Ожидалось исключение для неправильной длины")
    except ValueError as e:
        assert str(e) == "Предложенное слово состоит не из пяти символов",\
            "Некорректное сообщение об ошибке"


def test_try_guess_wrong_alphabet():
    """Проверка обработки слова из иных символов."""
    room = Room(room_id=1)
    try:
        room.try_guess("apple")
        raise AssertionError("Ожидалось исключение для неправильных символов")
    except ValueError as e:
        assert str(e) == "Предложенное слово содержит иные символы, кроме букв русского алфавита",\
            "Некорректное сообщение об ошибке"


def test_try_guess_partial_match():
    """Проверка частичного совпадения."""
    room = Room(room_id=1)
    room.word = "ПЯТКА"
    response = room.try_guess("пячка")
    assert response == [2, 2, 0, 2, 2], "Некорректный ответ для частичного совпадения"


def test_is_finished_correct_guess():
    """Проверка завершения игры при правильной догадке."""
    room = Room(room_id=1)
    room.word = "ПЯТКА"
    assert room.is_finished("пятка"), "Игра должна завершиться при правильном ответе"


def test_is_finished_max_attempts():
    """Проверка завершения игры при максимальном числе попыток."""
    room = Room(room_id=1)
    room.attempts = 0
    assert room.is_finished("ччччч"), "Игра должна завершиться при окончании попыток"


def test_try_guess_letter_in_word():
    """Проверка случая, когда буква есть в слове, но на другой позиции."""
    room = Room(room_id=1)
    room.word = "ПЯТКА"
    attempts = room.attempts
    response = room.try_guess("цапля")  # Буквы 'а', 'я' и 'п' есть в 'ПЯТКА', но на другой позиции
    assert response == [0, 1, 1, 0, 1], "Некорректный ответ для буквы в слове, но не на позиции"
    assert room.attempts == attempts - 1, "Счетчик оставшихся попыток должен уменьшиться"
