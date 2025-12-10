"""
Проект - сохранение и загрузка
"""

from dataclasses import dataclass, field
from typing import List, Optional
from pathlib import Path
import json
import uuid
from datetime import datetime

from .room import Room
from .furniture import Furniture


@dataclass
class Project:
    """Проект дизайна интерьера"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Новый проект"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    modified_at: str = field(default_factory=lambda: datetime.now().isoformat())

    rooms: List[Room] = field(default_factory=list)
    furniture: Furniture = field(default_factory=Furniture)

    # Метаданные проекта
    author: str = ""
    description: str = ""

    # Путь к файлу (если сохранён)
    file_path: Optional[str] = None

    def add_room(self, room: Room):
        """Добавить комнату"""
        self.rooms.append(room)
        self._update_modified()

    def remove_room(self, room_id: str):
        """Удалить комнату"""
        self.rooms = [r for r in self.rooms if r.id != room_id]
        self._update_modified()

    def get_room_by_id(self, room_id: str) -> Optional[Room]:
        """Получить комнату по ID"""
        for room in self.rooms:
            if room.id == room_id:
                return room
        return None

    def _update_modified(self):
        """Обновить время изменения"""
        self.modified_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        """Сериализация в словарь"""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
            "rooms": [r.to_dict() for r in self.rooms],
            "furniture": self.furniture.to_dict(),
            "author": self.author,
            "description": self.description,
            "version": "1.0"
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Project':
        """Десериализация из словаря"""
        return cls(
            id=data["id"],
            name=data["name"],
            created_at=data["created_at"],
            modified_at=data["modified_at"],
            rooms=[Room.from_dict(r) for r in data["rooms"]],
            furniture=Furniture.from_dict(data["furniture"]),
            author=data.get("author", ""),
            description=data.get("description", "")
        )

    def save(self, file_path: Optional[str] = None) -> str:
        """Сохранить проект в файл"""
        if file_path:
            self.file_path = file_path

        if not self.file_path:
            raise ValueError("Не указан путь для сохранения")

        # Убеждаемся что расширение .dizain
        path = Path(self.file_path)
        if path.suffix != ".dizain":
            path = path.with_suffix(".dizain")
            self.file_path = str(path)

        self._update_modified()

        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

        return self.file_path

    @classmethod
    def load(cls, file_path: str) -> 'Project':
        """Загрузить проект из файла"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        project = cls.from_dict(data)
        project.file_path = file_path
        return project

    @property
    def total_area(self) -> float:
        """Общая площадь всех комнат в м²"""
        return sum(room.floor_area for room in self.rooms)

    def get_summary(self) -> dict:
        """Получить сводку по проекту"""
        return {
            "total_rooms": len(self.rooms),
            "total_area": round(self.total_area, 2),
            "total_furniture": len(self.furniture.items),
            "rooms": [
                {
                    "name": room.name,
                    "area": round(room.floor_area, 2),
                    "walls": len(room.walls)
                }
                for room in self.rooms
            ]
        }
