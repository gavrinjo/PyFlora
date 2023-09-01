from app.functions import bp



@bp.app_template_filter()
def splitvalue(value, start=None, end=None):
    value = str(value)

    if start is None:
        start = 0
    if type(start) is int:
        start = start
    else:
        start = value.find(start) + len(start)

    if type(end) is int:
        end = end
    else:
        end = value.find(end)

    return value[start:end]

@bp.app_template_filter()
def round_value(value):
    if type(value) is str:
        return round(float(value))
    else:
        return round(value)