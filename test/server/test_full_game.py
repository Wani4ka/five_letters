import logging
from random import choice

from test.server import call_create_room, call_try_guess
from words import words

LOGGER = logging.getLogger(__name__)

def test_server_full_game():
    """Тест для прогона позитивного сценария полной игры"""
    room_id, attempts = call_create_room()

    while attempts > 0:
        attempts -= 1
        guess = choice(words)
        r = call_try_guess(room_id, guess)
        LOGGER.info("%s -> %s", guess, r.text)
        assert r.status_code in [200, 205],\
            f"Код ответа должен быть 200 или 205, получен {r.status_code}"
        response = r.json()

        assert "response" in response, "Должно присутствовать поле response"
        assert len(response["response"]) == 5, "Поле response должно содержать ровно 5 элементов"
        for entry in response["response"]:
            assert entry in [0, 1, 2], "Каждый элемент поля response должен быть равен 0, 1 или 2"

        match r.status_code:
            case 200:
                assert "attempts" in response,\
                    "Так как получен код 200, должно присутствовать количество оставшихся попыток"
                assert response["attempts"] > 0,\
                    "Количество оставшихся попыток должно быть положительным"
                assert "solution" not in response,\
                    "Так как получен код 200, не должно быть поля solution"

            case 205:
                assert "solution" in response,\
                    "Так как получен код 205, должно присутствовать поле solution"
                assert "attempts" not in response,\
                    "Так как получен код 205, не должно быть поля attempts"
                if response["solution"].upper() != guess.upper():
                    assert attempts == 0,\
                        ("Так как получен код 205, а верный ответ не найден,"
                         "это должна была быть последняя попытка")
