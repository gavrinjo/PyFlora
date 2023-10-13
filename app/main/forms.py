from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, Email
from app.models import User


class EditProfileForm(FlaskForm):
    # username = StringField('Username', validators=[DataRequired()])
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

    # def validate_username(self, username):
    #     if username.data != self.original_username:
    #         user = User.query.filter_by(username=self.username.data).first()
    #         if user is not None:
    #             raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError('Please use difernet email address!')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')