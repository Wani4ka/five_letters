from test.server import call_create_room, call_try_guess


def test_server_try_guess_incorrect_length():
    room_id, _ = call_create_room()
    r = call_try_guess(room_id, "МЕШОКК")
    assert r.status_code == 400, 'Должен возвращаться код ответа 400 "Bad Request"'
    response = r.json()

    assert "error" in response, "Должно присутствовать описание ошибки"
    assert (response["error"] ==
            "Предложенное слово состоит не из пяти символов"),\
        "Текст ошибки должен быть согласно спецификации"


def test_server_try_guess_invalid_word():
    room_id, _ = call_create_room()
    r = call_try_guess(room_id, "12345")
    assert r.status_code == 400, 'Должен возвращаться код ответа 400 "Bad Request"'
    response = r.json()

    assert "error" in response, "Должно присутствовать описание ошибки"
    assert (response["error"] ==
            "Предложенное слово содержит иные символы, кроме букв русского алфавита"),\
        "Текст ошибки должен быть согласно спецификации"


def test_server_try_guess_invalid_room_id():
    r = call_try_guess(2147483647, "МЕШОК")
    assert r.status_code == 404, 'Должен возвращаться код ответа 404 "Not Found"'
    response = r.json()

    assert "error" in response, "Должно присутствовать описание ошибки"
    assert (response["error"] ==
            "Комната с таким идентификатором не существует или игра в ней была завершена"),\
        "Текст ошибки должен быть согласно спецификации"
