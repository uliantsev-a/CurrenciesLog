# project/api/routes.py

from flask import Blueprint, request, jsonify
from project.auth import auth_required
from project.models.trades import Currency
from project.api.serializers import CurrencyListSchema
from project.api.exceptions import InvalidUsage

mod_api = Blueprint('api', __name__,)


@mod_api.route('/currencies')
@auth_required
def list_currencies():
    """
    Example request with paginate /api/currencies?page=1&perPage=3
    :return: Currencies list

    """
    params = request.args.to_dict()
    try:
        page = int(params.get('page', 1))
        per_page = int(params.get('perPage', None))
    except TypeError:
        raise InvalidUsage('Wrong query use', status_code=410)

    currencies = Currency.query.paginate(page, per_page, False)
    curr_schema = CurrencyListSchema()
    return jsonify(curr_schema.dump(currencies, many=False))
