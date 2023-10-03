from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField, BooleanField, Form, FormField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange
from app.models import Plant


class Testiram(Form):
    min_value = IntegerField('MIN', validators=[DataRequired()])
    max_value = IntegerField('MAX', validators=[DataRequired()])


class AddPlantForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    photo = FileField('Image file', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    sunlight = FormField(Testiram, 'Sunlight', render_kw=dict(unit='lux', popover_text='Osvjetljenje u rasponu od 0 luxa do 100000 luxa, normalno vanjsko osvjetljenje izeđu 300 i 750 luxa'))
    temperature = FormField(Testiram, 'Temperature', render_kw=dict(unit='°C', popover_text='Temperatura u rasponu od -20°C do 80°C'))
    moisture = FormField(Testiram, 'Moisture', render_kw=dict(unit='%', popover_text='Moisture u rasponu od 0% do 100%'))
    reaction = FormField(Testiram, 'Reaction', render_kw=dict(unit='pH', popover_text='Reaction u rasponu od 1pH do 14pH'))
    nutrient = FormField(Testiram, 'Nutrient', render_kw=dict(unit='%', popover_text='Nutrient u rasponu od 0% do 100%'))
    salinity = FormField(Testiram, 'Salinity', render_kw=dict(unit='%', popover_text='Salinity u rasponu od 0% do 100%'))
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

