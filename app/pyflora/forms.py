from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange
from app.models import Plant


class AddPlantForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    photo = FileField('Image file', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])

    l_min = IntegerField('Light min. Value [lux]', validators=[DataRequired(), NumberRange(min=0, max=100000)])
    l_max = IntegerField('Light max. Value [lux]', validators=[DataRequired(), NumberRange(min=0, max=100000)])

    t_min = IntegerField('Temperature min. Value [°C]', validators=[DataRequired(), NumberRange(min=-20, max=60)])
    t_max = IntegerField('Temperature max. Value [°C]', validators=[DataRequired(), NumberRange(min=-20, max=60)])

    f_min = IntegerField('Moisture min. Value [%]', validators=[DataRequired(), NumberRange(min=0, max=100)])
    f_max = IntegerField('Moisture max. Value [%]', validators=[DataRequired(), NumberRange(min=0, max=100)])

    r_min = IntegerField('Reaction min. Value [pH]', validators=[DataRequired(), NumberRange(min=0, max=14)])
    r_max = IntegerField('Reaction max. Value [pH]', validators=[DataRequired(), NumberRange(min=0, max=14)])

    n_min = IntegerField('Nutrient min. Value [%]', validators=[DataRequired(), NumberRange(min=0, max=100)])
    n_max = IntegerField('Nutrient max. Value [%]', validators=[DataRequired(), NumberRange(min=0, max=100)])

    s_min = IntegerField('Salinity min. Value [%]', validators=[DataRequired(), NumberRange(min=0, max=100)])
    s_max = IntegerField('Salinity max. Value [%]', validators=[DataRequired(), NumberRange(min=0, max=100)])

    soil_texture = SelectField('Soil texture', choices=['Fine', 'Medium', 'Coarse'])
    substrate = StringField('Substrate recomendation')
    description = TextAreaField('Description', validators=[Length(min=0, max=256)])
    submit = SubmitField('Submit')

    def __init__(self, original_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_name=original_name

    def validate_name(self, name):
        if name.data != self.original_name:
            plant = Plant.query.filter_by(name=name.data).first()
            if plant is not None:
                raise ValidationError('Please use difernet name!')


class PotForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    plant = SelectField('Select plant', coerce=int) # , validators=[DataRequired()]
    description = TextAreaField('Description', validators=[Length(min=0, max=256)])
    submit = SubmitField('Submit')


class EditPotForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    plant = SelectField('Select plant', coerce=int) # , validators=[DataRequired()]
    description = TextAreaField('Description', validators=[Length(min=0, max=256)])

    sunlight = BooleanField('Light sensor')
    # temperature_status = BooleanField('Temperature')
    moisture = BooleanField('Moisture sensor')
    reaction = BooleanField('pH reaction sensor')
    nutrient = BooleanField('Nutrient sensor')
    salinity = BooleanField('Salinity sensor')

    submit = SubmitField('Submit')

    def __init__(self, original_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_name=original_name

