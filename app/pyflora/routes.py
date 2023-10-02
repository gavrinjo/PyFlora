import os
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models import User, Plant, Pot
from app.pyflora import bp
from app.pyflora.forms import AddPlantForm, PotForm, EditPotForm
from app.main.forms import EditProfileForm, EmptyForm
from app.repo import upload_image


@bp.route('/explore/pyplants')
@login_required
def pyplants():
    plants = Plant.query.all()
    return render_template('pyflora/plant_list.html', title='PyPlants', plants=plants)

@bp.route('/plant/new', methods=['GET', 'POST'])
@login_required
def new_plant():
    form = AddPlantForm('')
    if form.validate_on_submit():
        plant = Plant(
            name=form.name.data,
            sunlight=f'{form.l_min.data};{form.l_max.data}',
            temperature=f'{form.t_min.data};{form.t_max.data}',
            moisture=f'{form.f_min.data};{form.f_max.data}',
            reaction=f'{form.r_min.data};{form.r_max.data}',
            nutrient=f'{form.n_min.data};{form.n_max.data}',
            salinity=f'{form.s_min.data};{form.s_max.data}',
            soil_texture=form.soil_texture.data,
            substrate=form.substrate.data,
            description=form.description.data
        )
        photo = upload_image(form.photo.data, 'plants')
        plant.photo = photo
        db.session.add(plant)
        db.session.commit()
        flash(f'Congratulations, Plant {plant.name} added secessefuly!', 'success')
        return redirect(url_for('main.index'))
    return render_template('pyflora/plant_new.html', title='Add PyPlant', form=form)