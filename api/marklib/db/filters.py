

def values_filter(query, field, values):
    if isinstance(values, basestring):
        values = list(values)
    query = query.filter(field.in_(values))
    return query
