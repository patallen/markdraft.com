from sqlalchemy import or_, asc, desc
from collections import OrderedDict


def values_filter(query, field, values):
    if isinstance(values, basestring):
        values = [values]
    query = query.filter(field.in_(values))
    return query


def contains_string(query, fields, value):
    if not hasattr(fields, '__iter__'):
        fields = (fields, )

    filters = []
    for field in fields:
        filters.append(field.ilike('%{}%'.format(value)))

    return query.filter(or_(*filters))


def limit_and_offset(query, page=None, rows=None):
    limit = int(rows or 25)
    page = int(page or 1)
    offset = limit * (page-1)
    query = query.limit(limit).offset(offset)
    return query


def parse_sort_string(sort_string):
    sorts = sort_string.split(',')
    parsed = OrderedDict()
    for item in sorts:
        split = item.split(' ')
        parsed[split[0]] = split[1]
    return parsed


def sort_query(query, model, sort_string):
    """
    Function for sorting a query based on the sort string
    provided in the url params.
    """
    if not sort_string:
        return query

    sorts = parse_sort_string(sort_string)
    for sort_by, direction in sorts.iteritems():
        if direction == 'desc':
            sort_func = desc
        if direction == 'asc':
            sort_func = asc

        query = query.order_by(sort_func(getattr(model, sort_by)))
    return query
