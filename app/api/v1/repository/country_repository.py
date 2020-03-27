from operator import and_
from typing import List

from sqlalchemy import desc, asc

from app.models import Records


class CountryRepository:

    def get_country_historic_data(self, country_iso) -> List[Records]:
        return Records.query.filter_by(country_iso=country_iso.upper()).all()

    def get_country_record_on_date(self, country_iso: str, date: str) -> Records:
        return Records.query.filter(Records.country_iso == country_iso).filter(Records.date == date).first()

    def get_latest_country_record(self, country_iso: str) -> Records:
        date = Records.query.filter(Records.country_iso == "IND").order_by(desc(Records.date)).first().date
        return self.get_country_record_on_date(country_iso, date)

    def get_country_timeseries(self, country_iso: str, from_date: str, to_date: str) -> List[Records]:
        return Records.query.filter(Records.country_iso == country_iso).filter(
            and_(Records.date >= from_date, Records.date < to_date)).order_by(asc(Records.date)).all()

    def get_latest_record_date(self) -> str:
        return Records.query.filter(Records.country_iso == "IND").order_by(desc(Records.date)).first().date

    def get_all_countries(self) -> List[Records]:
        return Records.query.distinct(Records.country_iso).all()
