from abc import ABC, abstractmethod

from game.room import Room

RoomNotFoundError = KeyError(
    "Комната с таким идентификатором не существует или игра в ней была завершена"
)



class BaseStorage(ABC):

    @abstractmethod
    def random_word(self) -> str:
        """Возвращает рандомное слово из хранилища"""
        pass

    @abstractmethod
    def save_room(self, room: Room):
        """Сохраняет новую комнату и назначает ей ID"""
        pass

    @abstractmethod
    def get_room(self, room_id: str) -> Room:
        """Возвращает по ID комнаты объект комнаты"""
        pass

    @abstractmethod
    def update_room(self, room: Room):
        """Обновляет комнату"""
        pass

    @abstractmethod
    def delete_room(self, room_id: str) -> None:
        """Удаляет комнату"""
        pass
