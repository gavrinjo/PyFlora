from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.main import bp
from app.models import User, Pot
from app.main.forms import EditProfileForm, EmptyForm


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
    user = User.query.filter_by(username=username).first_or_404()
    pots = Pot.query.filter_by(user_id=user.id).all()

    return render_template('user.html', title=username, user=user, pots=pots, form=form)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Changes have been saved!', 'success')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)
    
"""
@bp.route('/pot/<pot_id>/sync', methods=['POST'])
@login_required
def sync_pot(pot_id):
    form = EmptyForm()
    if form.validate_on_submit():
        pot = Pot.query.get(pot_id)
        measurement = SensorMeasurements.query.filter_by(pot_id=pot.id).order_by(SensorMeasurements.measured.desc()).first()

        new_measurement = SensorSim(pot, measurement).generate()

        db.session.add(new_measurement)
        db.session.commit()
        return redirect(url_for('main.view_pot', pot_id=pot.id))


@bp.route('/weather')
@login_required
def weather():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    cwd = Weather('Zagreb')
    return render_template('weather.html', title='Weather', cwd=cwd)
"""