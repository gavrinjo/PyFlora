from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange
from app.models import User, Plant


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=256)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username=original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class AddPlantForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    photo = FileField('Image file', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])

    l_min = IntegerField('Light min. Value [lux]', validators=[NumberRange(min=0, max=100000)])
    l_max = IntegerField('Light max. Value [lux]', validators=[NumberRange(min=0, max=100000)])

    t_min = IntegerField('Temperature min. Value [°C]', validators=[NumberRange(min=-20, max=60)])
    t_max = IntegerField('Temperature max. Value [°C]', validators=[NumberRange(min=-20, max=60)])

    f_min = IntegerField('Moisture min. Value [%]', validators=[NumberRange(min=0, max=100)])
    f_max = IntegerField('Moisture max. Value [%]', validators=[NumberRange(min=0, max=100)])

    r_min = IntegerField('Reaction min. Value [pH]', validators=[NumberRange(min=0, max=14)])
    r_max = IntegerField('Reaction max. Value [pH]', validators=[NumberRange(min=0, max=14)])

    n_min = IntegerField('Nutrient min. Value [%]', validators=[NumberRange(min=0, max=100)])
    n_max = IntegerField('Nutrient max. Value [%]', validators=[NumberRange(min=0, max=100)])

    s_min = IntegerField('Salinity min. Value [%]', validators=[NumberRange(min=0, max=100)])
    s_max = IntegerField('Salinity max. Value [%]', validators=[NumberRange(min=0, max=100)])

    # sunlight = SelectField('Sunlight', coerce=int)


    # salinity = SelectField('Salinity', validators=[DataRequired()], choices=['Low', 'Medium', 'High'])
    # temperature = IntegerField('Temperature', validators=[DataRequired(), NumberRange(min=0, max=40)])
    # ph_range = SelectField('PH range', validators=[DataRequired()], choices=['Acidic', 'Neutral', 'Alkaline'])
    # moisture = SelectField('Moisture', validators=[DataRequired()], choices=['Low', 'Medium', 'High'])
    # shade = SelectField('Shade', validators=[DataRequired()], choices=['Intolerant', 'Intermediate', 'Tolerant'])
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
