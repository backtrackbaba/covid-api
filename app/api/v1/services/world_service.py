from typing import List

from app.api.v1.repository.world_repository import WorldRepository


class WorldService:
    def __init__(self):
        self.world_repository = WorldRepository()

    def get_global_count(self) -> List:
        return self.world_repository.get_global_count()

    def get_global_count_on_date(self, date: str) -> List:
        return self.world_repository.get_global_count_on_date(date)
