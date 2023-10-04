import os
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models import User, Plant, Value, Pot
from app.pyflora import bp
from app.pyflora.forms import PlantForm, PotForm
from app.main.forms import EditProfileForm, EmptyForm
from app.repo import upload_image


@bp.route('/plant/list')
@login_required
def list_plant():
    plants = Plant.query.all()
    return render_template('pyflora/plant_list.html', title='PyPlants', plants=plants)

@bp.route('/plant/new', methods=['GET', 'POST'])
@login_required
def new_plant():
    form = PlantForm('')
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
        return redirect(url_for('pyflora.list_plant'))
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
    form = PlantForm(plant.name)
    if form.validate_on_submit():
        plant = Plant()
        plant.name = form.name.data
        plant.description = form.description.data
        plant.substrate = form.substrate.data
        photo = upload_image(form.photo.data, 'plants')
        plant.photo = photo
        for value in values:
                value.min_value = getattr(form, value.indicator.lower()).min_value.data
                value.max_value = getattr(form, value.indicator.lower()).max_value.data
        db.session.commit()
        flash(f'Congratulations, Plant {plant.name} updated secessefuly!', 'success')
        return redirect(url_for('pyflora.view_plant', plant_id=plant_id))
    elif request.method == 'GET':
        form.name.data = plant.name
        form.substrate.data = plant.substrate
        form.description.data = plant.description
        for value in values:
            getattr(form, value.indicator.lower()).min_value.data = value.min_value
            getattr(form, value.indicator.lower()).max_value.data = value.max_value
    return render_template('pyflora/plant_new.html', title='Update PyPlant', form=form)

@bp.route('/plant/<plant_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    name = plant.name
    os.remove(os.path.join(current_app.config['UPLOADS_DEFAULT_DEST'], f'plants/{plant.photo}'))
    db.session.delete(plant)
    db.session.commit()
    flash(f'Congratulations, Plant {name} deleted secessefuly!', 'success')
    return redirect(url_for('pyflora.list_plant'))

@bp.route('/pot/list')
@login_required
def list_pot():
    pots = Pot.query.all()
    return render_template('pyflora/pot_list.html', title='PyPlants', pots=pots)

@bp.route('/pot/<pot_id>')
@login_required
def view_pot(pot_id):
    pass
    # form = EmptyForm()
    # pot = Pot.query.get(pot_id)
    # fig = ZaPlotlyLine(pot).configure()
    # graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # return render_template('view_pot.html', title=pot.name, pot=pot, form=form, graphJSON=graphJSON)

@bp.route('/pot/new', methods=['GET', 'POST'])
@login_required
def new_pot():
    
    plants = Plant.query.all()
    plant_list = [(i.id, i.name) for i in plants]
    form = PotForm('')
    form.plant.choices = plant_list
    if form.validate_on_submit():
        plant = Plant.query.get(form.plant.data)
        pot = Pot()
        pot.name=form.name.data
        pot.description=form.description.data
        pot.user_id.owner=current_user
        pot.plant=plant
        db.session.add(pot)
        db.session.commit()
        flash(f'Congratulations, Pot {pot.name} added secessefuly!', 'success')
        return redirect(url_for('pyflora.list_pot'))
    return render_template('pyflora/pot_new.html', title='Add PyPot', form=form)


@bp.route('/pot/<pot_id>/update', methods=['GET', 'POST'])
@login_required
def update_pot(pot_id):
    pass
    # pot = Pot.query.get_or_404(pot_id)
    # plants = Plant.query.all()
    # plant_list = [(i.id, i.name) for i in plants]
    # form = EditPotForm(pot.name)
    # form.plant.choices = plant_list
    # if form.validate_on_submit():
    #     plant = Plant.query.get(form.plant.data)
    #     pot.name=form.name.data
    #     pot.description=form.description.data
    #     pot.plant=plant
    #     pot.sunlight_status = form.sunlight.data
    #     pot.moisture_status = form.moisture.data
    #     pot.reaction_status = form.reaction.data
    #     pot.nutrient_status = form.nutrient.data
    #     pot.salinity_status = form.salinity.data
    #     db.session.commit()
    #     flash(f'Congratulations, Pot {pot.name} updated secessefuly!', 'success')
    #     return redirect(url_for('main.pypots'))
    # elif request.method == 'GET':
    #     form.name.data = pot.name
    #     form.description.data = pot.description
    #     form.plant.data = pot.plant_id
    #     form.sunlight.data = pot.sunlight_status
    #     form.moisture.data = pot.moisture_status
    #     form.reaction.data = pot.reaction_status
    #     form.nutrient.data = pot.nutrient_status
    #     form.salinity.data = pot.salinity_status
    # return render_template('new_pot.html', title='Update PyPot', form=form)


@bp.route('/pot/<pot_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_pot(pot_id):
    pass
    # pot = Pot.query.get_or_404(pot_id)
    # name = pot.name
    # db.session.delete(pot)
    # db.session.commit()
    # flash(f'Congratulations, Pot {name} deleted secessefuly!', 'success')
    # return redirect(url_for('main.pypots'))


@bp.route('/pot/<pot_id>/sync', methods=['POST'])
@login_required
def sync_pot(pot_id):
    pass
    # form = EmptyForm()
    # if form.validate_on_submit():
    #     pot = Pot.query.get(pot_id)
    #     measurement = SensorMeasurements.query.filter_by(pot_id=pot.id).order_by(SensorMeasurements.measured.desc()).first()

    #     new_measurement = SensorSim(pot, measurement).generate()

    #     db.session.add(new_measurement)
    #     db.session.commit()
    #     return redirect(url_for('main.view_pot', pot_id=pot.id))