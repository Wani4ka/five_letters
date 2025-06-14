import requests

from test.server import call_create_room, call_try_guess, hostname


def test_server_try_guess_no_body():
    """Должна возвращаться ошибка, если ничего не передать"""
    room_id, _ = call_create_room()
    try:
        r = requests.post(
            f'{hostname}/rooms/{room_id}/attempts'
        )
    except Exception as e:
        raise AssertionError("Запрос должен выполниться без ошибок") from e
    assert r.status_code == 400, 'Должен возвращаться код ответа 400 "Bad Request"'
    response = r.json()

    assert "error" in response, "Должно присутствовать описание ошибки"
    assert (response["error"] ==
            "Некорректный формат JSON"),\
        "Текст ошибки должен быть о некорректном формате JSON"

def test_server_try_guess_invalid_type():
    """Должна возвращаться ошибка, если передать для проверки не строку"""
    room_id, _ = call_create_room()
    r = call_try_guess(room_id, 12345)
    assert r.status_code == 400, 'Должен возвращаться код ответа 400 "Bad Request"'
    response = r.json()

    assert "error" in response, "Должно присутствовать описание ошибки"
    assert (response["error"] ==
            "Поле 'guess' должно быть строкой"),\
        "Текст ошибки должен быть о поле guess"


def test_server_try_guess_incorrect_length():
    """Должна возвращаться ошибка, если передать для проверки слово некорректной длины"""
    room_id, _ = call_create_room()
    r = call_try_guess(room_id, "МЕШОКК")
    assert r.status_code == 400, 'Должен возвращаться код ответа 400 "Bad Request"'
    response = r.json()

    assert "error" in response, "Должно присутствовать описание ошибки"
    assert (response["error"] ==
            "Предложенное слово состоит не из пяти символов"),\
        "Текст ошибки должен быть согласно спецификации"


def test_server_try_guess_invalid_word():
    """Должна возвращаться ошибка, если передать невалидное слово для проверки"""
    room_id, _ = call_create_room()
    r = call_try_guess(room_id, "12345")
    assert r.status_code == 400, 'Должен возвращаться код ответа 400 "Bad Request"'
    response = r.json()

    assert "error" in response, "Должно присутствовать описание ошибки"
    assert (response["error"] ==
            "Предложенное слово содержит иные символы, кроме букв русского алфавита"),\
        "Текст ошибки должен быть согласно спецификации"


def test_server_try_guess_invalid_body():
    """Должна возвращаться ошибка, если передать невалидное тело для проверки"""
    room_id, _ = call_create_room()
    try:
        r = requests.post(
            f'{hostname}/rooms/{room_id}/attempts',
            data="not a json",
        )
    except Exception as e:
        raise AssertionError("Запрос должен выполниться без ошибок") from e

    assert r.status_code == 400, 'Должен возвращаться код ответа 400 "Bad Request"'
    response = r.json()

    assert "error" in response, "Должно присутствовать описание ошибки"
    assert (response["error"] == "Некорректный формат JSON"),\
        "Текст ошибки должен быть о некорректном формате JSON"


def test_server_try_guess_invalid_room_id():
    """Должна возвращаться ошибка, если передать невалидный ID комнаты"""
    r = call_try_guess(2147483647, "МЕШОК")
    assert r.status_code == 404, 'Должен возвращаться код ответа 404 "Not Found"'
    response = r.json()

    assert "error" in response, "Должно присутствовать описание ошибки"
    assert (response["error"] ==
            "Комната с таким идентификатором не существует или игра в ней была завершена"),\
        "Текст ошибки должен быть согласно спецификации"

def test_server_try_guess_nan_room_id():
    """Должна возвращаться ошибка, если передать нечисловой ID комнаты"""
    r = call_try_guess("invalid", "МЕШОК")
    assert r.status_code == 404, 'Должен возвращаться код ответа 404 "Not Found"'
    response = r.json()

    assert "error" in response, "Должно присутствовать описание ошибки"
    assert (response["error"] ==
            "Неизвестный маршрут"),\
        "Эндпойнт не должен быть распознан"
