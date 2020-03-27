from app.api.v1.repository.common_repository import CommonRepository


class CommonService:
    def __init__(self):
        self.common_repository = CommonRepository()

    def get_latest_date(self):
        return self.common_repository.get_latest_date()

    def get_all_dates(self):
        return self.common_repository.get_all_dates()
