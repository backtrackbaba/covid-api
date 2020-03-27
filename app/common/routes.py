from flask import render_template
from sqlalchemy import desc

from app import cache
from app.common import bp
from app.models import Records


@bp.route('/')
@cache.cached()
def home():
    return render_template('index.html')


# Keeping this route here for now as this doesn't fit in the refactored version-wise blueprints structure.
@bp.route('/api/v1/latest-date')
@cache.cached()
def latest_date():
    latest_date = Records.query.filter(Records.country_iso == "IND").order_by(desc(Records.date)).first().date
    return str(latest_date)
