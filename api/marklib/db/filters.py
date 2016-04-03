from sqlalchemy import or_


def values_filter(query, field, values):
    if isinstance(values, basestring):
        values = list(values)
    query = query.filter(field.in_(values))
    return query


def contains_string(query, fields, value):
    if not hasattr(fields, '__iter__'):
        fields = tuple(fields)

    filters = []
    for field in fields:
        filters.append(field.ilike('%{}%'.format(value)))

    return query.filter(or_(*filters))
