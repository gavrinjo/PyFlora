from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.data_sim import SensorData
from app.main import bp
from app.models import User, Plant, Pot, SensorMeasurements
from app.main.forms import EditProfileForm, AddPlantForm, PotForm

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
        flash('Changes have been saved!', 'success')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)
    

@bp.route('/explore/pyplants')
@login_required
def pyplants():
    plants = Plant.query.all()
    return render_template('pyplants.html', title='PyPlants', plants=plants)


@bp.route('/plant/new', methods=['GET', 'POST'])
@login_required
def new_plant():
    form = AddPlantForm('')
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
        flash(f'Congratulations, Plant {plant.name} added secessefuly!', 'success')
        return redirect(url_for('main.index'))
    return render_template('new_plant.html', title='Add PyPlant', form=form)


@bp.route('/plant/<plant_id>')
@login_required
def view_plant(plant_id):
    plant = Plant.query.get(plant_id)
    return render_template('view_plant.html', title=plant.name, plant=plant)


@bp.route('/plant/<plant_id>/update', methods=['GET', 'POST'])
@login_required
def update_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    form = AddPlantForm(plant.name)
    if form.validate_on_submit():
        plant.name=form.name.data
        plant.salinity=form.salinity.data
        plant.temperature=form.temperature.data
        plant.ph_range=form.ph_range.data
        plant.moisture=form.moisture.data
        plant.shade=form.shade.data
        plant.soil_texture=form.soil_texture.data
        plant.substrate=form.substrate.data
        plant.description=form.description.data
        db.session.commit()
        flash(f'Congratulations, Plant {plant.name} updated secessefuly!', 'success')
        return redirect(url_for('main.pyplants'))
    elif request.method == 'GET':
        form.name.data = plant.name
        form.salinity.data = plant.salinity
        form.temperature.data = plant.temperature
        form.ph_range.data = plant.ph_range
        form.moisture.data = plant.moisture
        form.shade.data = plant.shade
        form.soil_texture.data = plant.soil_texture
        form.substrate.data = plant.substrate
        form.description.data = plant.description
    return render_template('add_pyplant.html', title='Update PyPlant', form=form)


@bp.route('/plant/<plant_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    name = plant.name
    db.session.delete(plant)
    db.session.commit()
    flash(f'Congratulations, Plant {name} deleted secessefuly!', 'success')
    return redirect(url_for('main.pyplants'))


@bp.route('/explore/pypots')
@login_required
def pypots():
    pots = Pot.query.all()
    return render_template('pypots.html', title='PyPlants', pots=pots)


@bp.route('/pot/<pot_id>')
@login_required
def view_pot(pot_id):
    pot = Pot.query.get(pot_id)
    return render_template('view_pot.html', title=pot.name, pot=pot)


@bp.route('/pot/new', methods=['GET', 'POST'])
@login_required
def new_pot():
    plants = Plant.query.all()
    plant_list = [(i.id, i.name) for i in plants]
    form = PotForm()
    form.plant.choices = plant_list
    if form.validate_on_submit():
        plant = Plant.query.get(form.plant.data)
        potty = Pot(name=form.name.data, description=form.description.data, owner=current_user, plant=plant)
        db.session.add(potty)
        db.session.commit()
        flash(f'Congratulations, Pot {potty.name} added secessefuly!', 'success')
        return redirect(url_for('main.index'))
    return render_template('new_pot.html', title='Add PyPot', form=form)


@bp.route('/pot/<pot_id>/update', methods=['GET', 'POST'])
@login_required
def update_pot(pot_id):
    pot = Pot.query.get_or_404(pot_id)
    plants = Plant.query.all()
    plant_list = [(i.id, i.name) for i in plants]
    form = PotForm()
    form.plant.choices = plant_list
    if form.validate_on_submit():
        plant = Plant.query.get(form.plant.data)
        pot.name=form.name.data
        pot.description=form.description.data
        pot.plant=plant
        db.session.commit()
        flash(f'Congratulations, Pot {pot.name} updated secessefuly!', 'success')
        return redirect(url_for('main.pypots'))
    elif request.method == 'GET':
        form.name.data = pot.name
        form.description.data = pot.description
    return render_template('new_pot.html', title='Update PyPot', form=form)


@bp.route('/pot/<pot_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_pot(pot_id):
    pot = Pot.query.get_or_404(pot_id)
    name = pot.name
    db.session.delete(pot)
    db.session.commit()
    flash(f'Congratulations, Pot {name} deleted secessefuly!', 'success')
    return redirect(url_for('main.pypots'))


@bp.route('/pot/<pot_id>/sync', methods=['GET', 'POST'])
@login_required
def sync_pot(pot_id):
    pot = Pot.query.get(pot_id)
    measurement = SensorMeasurements.query.filter_by(pot_id=pot.id).order_by(SensorMeasurements.measured.desc()).first()
    soil_ph_range, soil_salinity, soil_moisture = SensorData(measurement).data()
    measurement = SensorMeasurements(salinity=soil_salinity, moisture=soil_moisture, ph_range=soil_ph_range)
    measurement.measured = datetime.utcnow()
    measurement.pot = pot
    db.session.add(measurement)
    db.session.commit()
    return redirect(url_for('main.view_pot', pot_id=pot.id))
