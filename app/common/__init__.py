from flask import Blueprint

bp = Blueprint('common', __name__)

from app.common import routes
