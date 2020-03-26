from flask import Blueprint

bp = Blueprint('protected', __name__, url_prefix="/protected")

from app.protected import routes
