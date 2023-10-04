from app.functions import bp



@bp.app_template_filter()
def round_value(value):
    if type(value) is str:
        return round(float(value))
    else:
        return round(value)