import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

import storage_factory
from game.game import Game  # Импорт игровой логики

# Инициализация менеджера игры
game = Game(storage_factory.from_os_environ())


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

    def _parse_room_id(self, path: str) -> str | None:
        """Извлекает ID комнаты из пути вида /rooms/<room_id>/attempts"""
        parts = path.split("/")
        if len(parts) != 4 or parts[1] != "rooms" or parts[3] != "attempts":
            return None
        else:
            return parts[2]

    def _read_json_body(self) -> dict | None:
        """Читает и парсит JSON-тело запроса с обработкой ошибок"""
        content_length = int(self.headers.get("Content-Length", 0))
        if not content_length:
            return None

        try:
            body = self.rfile.read(content_length).decode("utf-8")
            return json.loads(body)
        except (UnicodeDecodeError, json.JSONDecodeError):
            return None

    def _handle_create_room(self):
        """Обработка создания новой игровой комнаты"""
        room = game.create_room()
        self._send_json(201, {"id": room.room_id, "attempts": room.attempts})

    def _handle_submit_attempt(self, room_id: str):
        """Обработка отправки попытки угадывания"""
        # Получение и валидация тела запроса
        payload = self._read_json_body()
        if not payload or not isinstance(payload, dict):
            self._send_json(400, {"error": "Некорректный формат JSON"})
            return

        # Валидация предположения
        guess = payload.get("guess")
        if not isinstance(guess, str):
            self._send_json(400, {"error": "Поле 'guess' должно быть строкой"})
            return

        # Обработка игровой логики
        try:
            response_list, finished, attempts, solution = game.try_guess(room_id, guess)
        except ValueError as e:
            self._send_json(400, {"error": str(e)})
            return
        except KeyError as e:
            self._send_json(404, {"error": str(e).strip("'")})
            return

        # Формирование ответа
        if finished:
            self._send_json(205, {"response": response_list, "solution": solution})
        else:
            self._send_json(200, {"response": response_list, "attempts": attempts})

    def do_POST(self):  # noqa: N802 название функции взято из документации библиотеки
        """Маршрутизация POST-запросов"""
        parsed = urlparse(self.path)
        path = parsed.path

        # Маршрутизация запросов
        if path == "/rooms":
            self._handle_create_room()
        else:
            room_id = self._parse_room_id(path)
            if room_id is not None:
                self._handle_submit_attempt(room_id)
            else:
                self._send_json(404, {"error": "Неизвестный маршрут"})


def run_server(host: str = "0.0.0.0", port: int = 8008):
    """Запуск HTTP-сервера на указанном хосте и порту"""
    server_address = (host, port)
    httpd = HTTPServer(server_address, WordleRequestHandler)
    print(f"Server start on {host}:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nОстановка сервера")
        httpd.server_close()


if __name__ == "__main__":
    run_server()
