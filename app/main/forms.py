from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, Email
from app.models import User


class EditProfileForm(FlaskForm):
    first_name = StringField('First name')
    last_name = StringField('Last name')
    email = StringField('Email', validators=[Email()])
    phone = StringField('Phone')
    mobile = StringField('Mobile phone')
    address = StringField('Address')
    postcode = StringField('Post code')
    city = StringField('City')
    country = StringField('Country')
    about_me = TextAreaField('About me', validators=[Length(min=0, max=256)])
    submit = SubmitField('Submit')

    def __init__(self, original_email, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_email=original_email
   
    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError('Please use difernet email address!')


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=128, max=1024)])
    submit = SubmitField('Submit')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')