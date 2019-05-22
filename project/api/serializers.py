from marshmallow import fields, Schema

from project import ma
from project.models.trades import Currency, Rate


class PagedListSchema(Schema):
    has_prev = fields.Integer(dump_to='hasPrev', dump_only=True)
    has_next = fields.Integer(dump_to='hasNext', dump_only=True)
    prev_num = fields.Integer(dump_to='prev', dump_only=True)
    next_num = fields.Integer(dump_to='next', dump_only=True)
    page = fields.Integer(dump_to='page', dump_only=True)
    pages = fields.Integer(dump_to='pages', dump_only=True)
    per_page = fields.Integer(dump_to='perPage', dump_only=True)
    total = fields.Integer(dump_to='total', dump_only=True)


class CurrencySchema(ma.ModelSchema):

    class Meta:
        model = Currency
        fields = ('name',)


class CurrencyListSchema(PagedListSchema):
    items = fields.Nested(CurrencySchema, many=True, dump_only=True)


class RateSchema(ma.ModelSchema):
    average = fields.Function(lambda obj: obj.currency.average_from_period())
    last_rate = fields.Float(attribute="rate")

    class Meta:
        model = Rate
        fields = ('date', 'last_rate', 'average')
