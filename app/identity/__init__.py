from flask import Blueprint

bp = Blueprint('identity', __name__)

from app.identity import routes
