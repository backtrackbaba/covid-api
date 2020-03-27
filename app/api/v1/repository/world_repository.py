from typing import List

from sqlalchemy import desc

from app.models import Records


class WorldRepository:

    def get_global_count(self) -> List:
        date = Records.query.filter(Records.country_iso == "IND").order_by(desc(Records.date)).first().date
        return self.get_global_count_on_date(date)

    def get_global_count_on_date(self, date: str) -> List:
        return Records.query.filter(Records.date == date).all()
