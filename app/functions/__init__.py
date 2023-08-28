from flask import Blueprint

bp = Blueprint('filters', __name__)

from app.main import routes