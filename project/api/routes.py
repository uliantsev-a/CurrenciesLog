# project/api/routes.py

from flask import Blueprint

mod_api = Blueprint('api', __name__,)


@mod_api.route('/')
def get_tickers():
    return 'Home'
