from datetime import date
from typing import List

from app.api.v1.repository.common_repository import CommonRepository
from app.models import Records


class CommonService:
    def __init__(self):
        self.common_repository = CommonRepository()

    def get_latest_date(self) -> date:
        return self.common_repository.get_latest_date()

    def get_all_dates(self) -> List[Records]:
        return self.common_repository.get_all_dates()
