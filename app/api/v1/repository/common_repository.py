from sqlalchemy import desc

from app.models import Records


class CommonRepository:

    def get_latest_date(self):
        return Records.query.filter(Records.country_iso == "IND").order_by(desc(Records.date)).first().date

    def get_all_dates(self):
        return Records.query.distinct(Records.date).all()
