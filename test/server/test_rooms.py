import requests

from test.server import call_create_room, hostname


def test_server_create_room():
    """Комната должна создаться успешно"""
    call_create_room()


def test_server_invalid_endpoint():
    """Должна возвращаться ошибка, если вызвать невалидный эндпойнт"""
    try:
        r = requests.post(f'{hostname}/invalid')
    except Exception as e:
        raise AssertionError("Запрос должен выполниться без ошибок") from e
    assert r.status_code == 404,\
        f'Должен возвращаться код ответа 404 "Not Found", получен "{r.status_code}"'

    response = r.json()
    assert "error" in response, "Должно присутствовать описание ошибки"
    assert (response["error"] ==
            "Неизвестный маршрут"),\
        f'Текст ошибки должен сообщать о невалидном эндпойнте, получено "{response["error"]}"'
