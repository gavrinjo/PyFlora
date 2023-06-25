from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.main import bp
from app.models import User, Plant
from app.main.forms import EditProfileForm, AddPlantForm

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
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', title=username, user=user, posts=posts)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Changes have been saved!')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)
    

@bp.route('/pyplants')
@login_required
def pyplants():
    plants = Plant.query.all()
    return render_template('pyplants.html', title='PyPlants', plants=plants)


@bp.route('/new_plant', methods=['GET', 'POST'])
@login_required
def new_plant():
    form = AddPlantForm()
    if form.validate_on_submit():
        plant = Plant(
            name=form.name.data,
            salinity=form.salinity.data,
            temperature=form.temperature.data,
            ph_range=form.ph_range.data,
            moisture=form.moisture.data,
            shade=form.shade.data,
            soil_texture=form.soil_texture.data,
            substrate=form.substrate.data,
            description=form.description.data
        )
        db.session.add(plant)
        db.session.commit()
        flash(f'Congratulations, Plant {plant.name} added secesseful!')
        return redirect(url_for('main.index'))
    return render_template('add_pyplant.html', title='Add PyPlant', form=form)