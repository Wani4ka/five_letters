import json

import requests

hostname = "http://localhost:8008"

def call_create_room() -> (str, int):
    try:
        r = requests.post(f'{hostname}/rooms')
    except Exception as e:
        raise AssertionError("Запрос должен выполниться без ошибок") from e
    assert r.status_code == 201, 'Должен возвращаться код ответа 201 "Created"'
    response = r.json()

    assert "id" in response, "Должен присутствовать корректный идентификатор комнаты"
    assert response["id"] != "", "Идентификатор комнаты не должен быть пустым"

    assert "attempts" in response, "Должно присутствовать корректное количество попыток"
    assert response["attempts"] > 0, "Количество попыток должно быть положительно"

    return response["id"], response["attempts"]

def call_try_guess(room_id: str, guess: str) -> requests.Response:
    try:
        r = requests.post(
            f'{hostname}/rooms/{room_id}/attempts',
            data=json.dumps({'guess': guess}),
        )
    except Exception as e:
        raise AssertionError("Запрос должен выполниться без ошибок") from e
    return r
