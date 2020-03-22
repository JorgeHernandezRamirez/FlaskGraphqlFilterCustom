import graphene
from graphene import types
from graphene_sqlalchemy_filter import FilterSet
from sqlalchemy import func, String

from model import UserModel

ALL_OPERATIONS = ['eq', 'ne', 'like', 'ilike', 'is_null', 'in', 'not_in', 'lt', 'lte', 'gt', 'gte', 'range', 'likeall']


def likeall_filter(field, value: str):
    return func.lower(func.cast(field, String)).like('%' + str(value).lower() + '%')


class MyFilterSet(FilterSet):
    LIKEALL = 'likeall'

    EXTRA_EXPRESSIONS = {
        'likeall': {
            'graphql_name': 'likeall',
            'for_types': [types.Date, types.DateTime, types.String, types.Int, types.Decimal],
            'filter': likeall_filter,
            'input_type': (
                lambda type_, nullable, doc: graphene.String(nullable=False)
            ),
            'description': 'Filter like for all types',
        }
    }

    class Meta:
        abstract = True


class UserFilter(MyFilterSet):
    class Meta:
        model = UserModel
        fields = {
            'userid': ALL_OPERATIONS,
            'name': ALL_OPERATIONS,
            'surname': ALL_OPERATIONS,
            'age': ALL_OPERATIONS,
        }
