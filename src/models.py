from sqlalchemy.dialects.postgresql import DATE, UUID

from src.app import db


class Records(db.Model):
    __tablename__ = 'records'
    __table_args__ = {'extend_existing': True}

    uuid = db.Column(UUID(as_uuid=True), primary_key=True)
    country_iso = db.Column(db.String(100), index=True)
    country_name = db.Column(db.String(100))
    date = db.Column(DATE)
    confirmed = db.Column(db.INTEGER)
    deaths = db.Column(db.INTEGER)
    recovered = db.Column(db.INTEGER)

    def __repr__(self):
        return f'<Record ID: {self.uuid}, ISO: {self.country_iso}, Country: {self.country_name}, Date: {self.date}, {self.confirmed, self.deaths, self.deaths}>'
