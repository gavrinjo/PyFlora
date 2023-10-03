import os
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models import User, Plant, Value, Pot
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
        plant = Plant()
        plant.name = form.name.data
        plant.description = form.description.data
        plant.substrate = form.substrate.data
        photo = upload_image(form.photo.data, 'plants')
        plant.photo = photo
        db.session.add(plant)
        db.session.flush()
        for field in form:
            if field.type == 'FormField':
                value = Value()
                value.indicator = field.label.text
                value.min_value = field.min_value.data
                value.max_value = field.max_value.data
                value.unit = field.render_kw['unit']
                value.plant_id = plant.id
                db.session.add(value)
        db.session.commit()
        flash(f'Congratulations, Plant {plant.name} added secessefuly!', 'success')
        return redirect(url_for('main.index'))
    return render_template('pyflora/plant_new.html', title='Add PyPlant', form=form)

@bp.route('/plant/<plant_id>')
@login_required
def view_plant(plant_id):
    form = EmptyForm()
    plant = Plant.query.get(plant_id)
    image_file = url_for('static', filename=f'plants/{plant.photo}')
    values = Value.query.filter_by(plant_id=plant_id).all()
    return render_template('pyflora/plant_view.html', title=plant.name, plant=plant, image_file=image_file, values=values, form=form)


@bp.route('/plant/<plant_id>/update', methods=['GET', 'POST'])
@login_required
def update_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    values = Value.query.filter_by(plant_id=plant.id).all()
    form = AddPlantForm(plant.name)
    if form.validate_on_submit():
        plant = Plant()
        plant.name = form.name.data
        plant.description = form.description.data
        plant.substrate = form.substrate.data
        # photo = upload_image(form.photo.data, 'plants')
        # plant.photo = photo
        for value in values:
                value.min_value = getattr(form, value.indicator.lower()).min_value.data
                value.max_value = getattr(form, value.indicator.lower()).max_value.data
        db.session.commit()
        flash(f'Congratulations, Plant {plant.name} updated secessefuly!', 'success')
        return redirect(url_for('pyflora.pyplants'))
    elif request.method == 'GET':
        form.name.data = plant.name
        form.substrate.data = plant.substrate
        form.description.data = plant.description
        for value in values:
            getattr(form, value.indicator.lower()).min_value.data = value.min_value
            getattr(form, value.indicator.lower()).max_value.data = value.max_value
        # form.photo.data = plant.photo # os.path.normpath(os.path.join(current_app.config['UPLOADS_DEFAULT_DEST'], 'plants', plant.photo)) # plant.photo
    return render_template('pyflora/plant_new.html', title='Update PyPlant', form=form)