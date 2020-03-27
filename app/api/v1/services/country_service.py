from typing import List

from app.api.v1.repository.country_repository import CountryRepository
from app.models import Records


class CountryService:
    def __init__(self):
        self.country_repository = CountryRepository()

    def get_country_historic_data(self, country_iso: str) -> List[Records]:
        return self.country_repository.get_country_historic_data(country_iso)

    def get_country_record_on_date(self, country_iso: str, date: str) -> Records:
        return self.country_repository.get_country_record_on_date(country_iso, date)

    def get_latest_country_record(self, country_iso: str) -> Records:
        return self.country_repository.get_latest_country_record(country_iso)

    def get_country_timeseries(self, country_iso: str, from_date: str, to_date: str) -> List[Records]:
        return self.country_repository.get_country_timeseries(country_iso, from_date, to_date)

    def get_latest_record_date(self) -> str:
        return self.country_repository.get_latest_record_date()

    def get_all_countries(self) -> List[Records]:
        return self.country_repository.get_all_countries()
