from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from app import db
from app.main import bp
from app.email import send_email
from app.models import User, Pot
from app.main.forms import EditProfileForm, EmptyForm, ContactForm, UploadForm
from app.resources.repo import upload_image
from app.resources.weather import Weather


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    # ovdje ide lista pyflora posuda
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


@bp.route('/user/<username>')
@login_required
def user(username):
    form = EmptyForm()
    upload_form = UploadForm()
    user = User.query.filter_by(username=username).first_or_404()
    pots = Pot.query.filter_by(user_id=user.id).all()

    return render_template('user.html', title=username, user=user, pots=pots, form=form, upload_form=upload_form)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.email)
    if form.validate_on_submit():
        # current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.mobile = form.mobile.data
        current_user.address = form.address.data
        current_user.postcode = form.postcode.data
        current_user.city = form.city.data
        current_user.country = form.country.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Changes have been saved!', 'success')
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        # form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.mobile.data = current_user.mobile
        form.address.data = current_user.address
        form.postcode.data = current_user.postcode
        form.city.data = current_user.city
        form.country.data = current_user.country
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        send_email(
        'PyFlora - Message submited',
        sender=current_app.config['ADMINS'][0],
        recipients=[form.email.data],
        text_body=render_template('email/contact_message.txt', user=form.name.data, message=form.message.data),
        html_body=render_template('email/contact_message.html', user=form.name.data, message=form.message.data)
        )
        send_email(
        f'PyFlora - {form.name.data} Message',
        sender=form.email.data,
        recipients=[current_app.config['ADMINS'][0]],
        text_body=render_template('email/contact_message.txt', user=form.name.data, message=form.message.data),
        html_body=render_template('email/contact_message.html', user=form.name.data, message=form.message.data)
        )
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('main.contact'))
    return render_template('contact_form.html', title='Contact us', form=form)
# @bp.route('/weather')
# @login_required
# def weather():
#     user = User.query.filter_by(username=current_user.username).first_or_404()
#     cwd = Weather('Zagreb')
#     return render_template('weather.html', title='Weather', cwd=cwd)
