from flask import render_template

from app import cache
from app.common import bp


@bp.route('/')
@cache.cached(timeout=86400, metrics=True)
def home():
    return render_template('index.html')
