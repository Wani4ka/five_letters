import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from game.game import Game  # Импорт игровой логики

# Инициализация менеджера игры
game = Game()

# Множество допустимых русских букв (в верхнем регистре)
RUSSIAN_LETTERS = set("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")


class WordleRequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, code: int, data: dict):
        """
        Вспомогательный метод для отправки JSON-ответа с заданным HTTP-статусом.
        """
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self):
        # Разбор URL для определения запрашиваемого эндпоинта
        parsed = urlparse(self.path)
        path = parsed.path

        # Эндпоинт: Создание новой игровой комнаты
        if path == "/rooms":
            room = game.create_room()
            # Возвращаем ID комнаты и максимальное количество попыток
            data = {"id": room.room_id, "attempts": room.max_attempts}
            self._send_json(201, data)  # 201 Created
            return

        # Эндпоинт: Отправка попытки угадывания
        if path.startswith("/rooms/"):
            parts = path.split("/")
            # Ожидаем путь вида: /rooms/<room_id>/attempts
            if len(parts) == 4 and parts[1] == "rooms" and parts[3] == "attempts":
                try:
                    room_id = int(parts[2])  # Парсим ID комнаты
                except ValueError:
                    # Некорректный ID комнаты
                    self._send_json(
                        404,
                        {
                            "error": "Комната с таким идентификатором не существует или игра в ней была завершена"
                        },
                    )
                    return

                # Проверка существования комнаты
                if room_id not in game.rooms:
                    self._send_json(
                        404,
                        {
                            "error": "Комната с таким идентификатором не существует или игра в ней была завершена"
                        },
                    )
                    return

                # Чтение тела запроса
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length).decode("utf-8")

                try:
                    payload = json.loads(body)  # Парсим JSON
                except json.JSONDecodeError:
                    self._send_json(400, {"error": "Некорректный формат JSON"})
                    return

                # Извлекаем предположение игрока
                guess = payload.get("guess")
                if not isinstance(guess, str):
                    self._send_json(400, {"error": "Поле 'guess' должно быть строкой"})
                    return

                # Валидация длины слова
                if len(guess) != 5:
                    self._send_json(
                        400, {"error": "Предложенное слово состоит не из пяти символов"}
                    )
                    return

                # Валидация символов (только русские буквы)
                for ch in guess:
                    up = ch.upper()
                    if up not in RUSSIAN_LETTERS:
                        self._send_json(
                            400,
                            {
                                "error": "Предложенное слово содержит иные символы, кроме букв русского алфавита"
                            },
                        )
                        return

                # Обработка попытки угадывания
                try:
                    room = game.rooms[room_id]  # Получаем объект комнаты
                    # Выполняем попытку и получаем результат
                    response_list, finished, solution = game.try_guess(room_id, guess)
                except Exception:
                    # Обработка ошибок доступа к комнате
                    self._send_json(
                        404,
                        {
                            "error": "Комната с таким идентификатором не существует или игра в ней была завершена"
                        },
                    )
                    return

                # Проверка завершения игры
                if finished:
                    # 205 Reset Content: игра завершена, возвращаем решение
                    self._send_json(205, {"response": response_list, "solution": solution})
                    return
                else:
                    # Игра продолжается, возвращаем оставшиеся попытки
                    attempts_left = room.max_attempts - room.attempts
                    self._send_json(200, {"response": response_list, "attempts": attempts_left})
                    return

        # Если эндпоинт не распознан
        self._send_json(404, {"error": "Неизвестный маршрут"})


def run_server(host: str = "0.0.0.0", port: int = 8008):
    """Запуск HTTP-сервера на указанном хосте и порту"""
    server_address = (host, port)
    httpd = HTTPServer(server_address, WordleRequestHandler)
    print(f"Server start on {host}:{port}")
    try:
        httpd.serve_forever()  # Бесконечный цикл обработки запросов
    except KeyboardInterrupt:
        print("\nОстановка сервера")
        httpd.server_close()


if __name__ == "__main__":
    run_server()  # Точка входа при запуске скрипта
