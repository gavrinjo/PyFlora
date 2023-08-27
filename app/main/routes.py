import os
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, abort, current_app
from flask_login import login_required, current_user
from app import db, weather
from app.data_sim import Sensor, Gauge
from app.main import bp
from app.models import User, Plant, Pot, SensorMeasurements
from app.main.forms import EditProfileForm, AddPlantForm, PotForm
from werkzeug.utils import secure_filename
from app.repo import Radar, Line, plant_needs

import matplotlib.pyplot as plt
import io
import base64
from matplotlib.figure import Figure
import numpy as np
import pandas as pd

temperature = round(float(weather.temperature[0]))
f_like = round(float(weather.feels_like[0]))

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
    return render_template('index.html', title='Home', posts=posts, temperature=temperature, f_like=f_like)


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
    attribs = plant_needs()
    form.sunlight.choices = attribs['sunlight']
    if form.validate_on_submit():
        sun = Gauge.query.get(form.sunlight.data)
        plant = Plant(
            name=form.name.data,
            salinity=form.salinity.data,
            temperature=form.temperature.data,
            ph_range=form.ph_range.data,
            moisture=form.moisture.data,
            shade=sun,
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
    image_file = url_for('static', filename=f'plants/{plant.photo}')
    return render_template('view_plant.html', title=plant.name, plant=plant, image_file=image_file)


@bp.route('/plant/<plant_id>/update', methods=['GET', 'POST'])
@login_required
def update_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    form = AddPlantForm(plant.name)
    if form.validate_on_submit():

        uploaded_file = request.files['photo']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in current_app.config['UPLOADED_FILES_ALLOW']:
                abort(400)
            uploaded_file.save(os.path.join(current_app.config['UPLOADS_DEFAULT_DEST'], 'plants', filename))

        plant.name=form.name.data
        plant.photo=filename
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
        form.photo.data = plant.photo
        form.salinity.data = plant.salinity
        form.temperature.data = plant.temperature
        form.ph_range.data = plant.ph_range
        form.moisture.data = plant.moisture
        form.shade.data = plant.shade
        form.soil_texture.data = plant.soil_texture
        form.substrate.data = plant.substrate
        form.description.data = plant.description
    return render_template('new_plant.html', title='Update PyPlant', form=form)


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
    metrics = SensorMeasurements

    query = (
        metrics.query
        .with_entities(metrics.measured, metrics.temperature, metrics.moisture, metrics.salinity, metrics.reaction, metrics.sunlight, metrics.nutrient)
        .filter_by(pot_id=pot_id)
        .order_by(metrics.measured.desc()).limit(7)
    )
    columns = ['measured', 'temperature', 'moisture', 'salinity', 'reaction', 'sunlight', 'nutrient']

    df = pd.DataFrame(query, columns=columns)

    # df = pd.DataFrame(metrics.query
    # .with_entities(metrics.salinity, metrics.ph_range, metrics.moisture)
    # .filter_by(pot_id=pot_id)
    # .order_by(metrics.measured.desc()).first(), columns=['salinity', 'ph_range', 'moisture'])

    # df = (metrics.query
    # .with_entities(metrics.salinity, metrics.ph_range, metrics.moisture)
    # .filter_by(pot_id=pot_id)
    # .order_by(metrics.measured.desc()).first())
    # df = [x for x in df]

    # df = pd.DataFrame(metrics.query
    # .with_entities(metrics.measured, metrics.moisture, metrics.salinity, metrics.reaction, metrics.sunlight, metrics.nutrient)
    # .filter_by(pot_id=pot_id)
    # .order_by(metrics.measured.desc()).limit(7)[::-1], columns=['measured', 'moisture', 'salinity', 'reaction', 'sunlight', 'nutrient'])

    # chart = Line()
    # chart.plot(df['measured'], np.log2(df['salinity'])*2, 'blue', 'salinity')
    # chart.plot(df['measured'], (df['reaction']/14)*10, 'red', 'reaction')
    # chart.plot(df['measured'], (df['moisture']/100)*10, 'orange', 'moisture')
    # data = chart.represent_chart()




    radar = Radar()

    # df = pd.DataFrame(metrics.query
    # .with_entities(metrics.temperature, metrics.moisture, metrics.salinity, metrics.reaction, metrics.sunlight, metrics.nutrient)
    # .filter_by(pot_id=pot_id)
    # .order_by(metrics.measured.desc()).limit(1), columns=['temperature', 'moisture', 'salinity', 'reaction', 'sunlight', 'nutrient'])

    data = []
    for i, val in enumerate(df.iloc[0][columns[1:]]):
        if i == 0:
           data.append(np.interp(val, [-20,80], [1,10]))
        else:
            data.append(np.interp(val, [0,100], [1,10]))

    radar.plot(columns[1:], data, 'green', 'measured')
    radar.plot(columns[1:], [5, 5, 5, 5, 5, 5], 'orange', 'neutral')
    data = radar.represent_chart()

    return render_template('view_pot.html', title=pot.name, pot=pot, data=data)


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
    sensor_data = Sensor(pot, measurement).build()
    db.session.add(sensor_data)
    db.session.commit()
    return redirect(url_for('main.view_pot', pot_id=pot.id))
