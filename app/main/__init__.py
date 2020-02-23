from flask import Blueprint

main_view = Blueprint('main_view', __name__)

from . import views