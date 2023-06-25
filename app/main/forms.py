from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
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
    salinity = SelectField('Salinity', validators=[DataRequired()], choices=['Low', 'Medium', 'High'])
    temperature = IntegerField('Temperature', validators=[DataRequired(), NumberRange(min=0, max=40)])
    ph_range = SelectField('PH range', validators=[DataRequired()], choices=['Acidic', 'Neutral', 'Alkaline'])
    moisture = SelectField('Moisture', validators=[DataRequired()], choices=['Low', 'Medium', 'High'])
    shade = SelectField('Shade', validators=[DataRequired()], choices=['Intolerant', 'Intermediate', 'Tolerant'])
    soil_texture = SelectField('Soil texture', validators=[DataRequired()], choices=['Fine', 'Medium', 'Coarse'])
    substrate = StringField('Substrate recomendation')
    description = TextAreaField('Description', validators=[Length(min=0, max=256)])
    submit = SubmitField('Submit')

    def validate_name(self, name):
        plant = Plant.query.filter_by(name=name.data).first()
        if plant is not None:
            raise ValidationError('Please use difernet name!')
