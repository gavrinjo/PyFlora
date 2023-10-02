from flask import Blueprint

bp = Blueprint('pyflora', __name__)

from app.pyflora import routes