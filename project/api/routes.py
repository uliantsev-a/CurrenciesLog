# project/api/routes.py

from flask import Blueprint, request, jsonify
from project.auth import auth_required
from project.models.trades import Currency, Rate
from project.api.serializers import RateSchema, CurrencyListSchema
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


@mod_api.route('/rate/<curr_id>')
@auth_required
def get_rate_info(curr_id):
    curr = Currency.query.get(curr_id)
    if curr is None:
        raise InvalidUsage('Not found currency', status_code=404)

    rate = (
        Rate.query.join(Rate.currency).filter(Currency.id == curr.id).
        order_by(Rate.date.desc()).first()
    )
    rate_schema = RateSchema(many=False)

    return rate_schema.jsonify(rate)
