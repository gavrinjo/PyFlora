import os
import plotly
import json
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Plant, Value, Pot, Sensor
from app.pyflora import bp
from app.pyflora.forms import PlantForm, PotForm
from app.main.forms import EmptyForm
from app.resources.repo import upload_image
from app.resources.sensors_sim import SensorSim
from app.resources.charts import PlotlyLine, PlotlyHisto, PlotlyPie, PLine


@bp.route('/plant/list')
@login_required
def list_plant():
    plants = Plant.query.all()
    return render_template('pyflora/plant_list.html', title='PyPlants', plants=plants)

@bp.route('/plant/<plant_id>')
@login_required
def view_plant(plant_id):
    form = EmptyForm()
    plant = Plant.query.get(plant_id)
    values = plant.values.all()
    return render_template('pyflora/plant_view.html', title=plant.name, plant=plant, values=values, form=form)

@bp.route('/plant/new', methods=['GET', 'POST'])
@login_required
def new_plant():
    form = PlantForm('')
    if form.validate_on_submit():
        plant = Plant()
        plant.name = form.name.data
        plant.description = form.description.data
        plant.soil_texture = form.soil_texture.data
        plant.substrate = form.substrate.data
        plant.wiki_url = form.wiki_url.data
        plant.other_url = form.other_url.data
        if form.photo.data:
            plant.photo = upload_image(form.photo.data, 'images/plants')
        db.session.add(plant)
        db.session.flush()
        for measure in current_app.config['MEASURES']:
            value = Value()
            value.indicator = measure
            value.min_value = getattr(form, measure).min_value.data
            value.max_value = getattr(form, measure).max_value.data
            value.unit = getattr(form, measure).render_kw['unit']
            value.plant = plant
            db.session.add(value)
        db.session.commit()
        flash(f'Congratulations, Plant {plant.name} added secessefuly!', 'success')
        return redirect(url_for('pyflora.list_plant'))
    return render_template('pyflora/plant_new.html', title='Add PyPlant', form=form)

@bp.route('/plant/<plant_id>/update', methods=['GET', 'POST'])
@login_required
def update_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    values = plant.values.all()
    form = PlantForm(plant.name)
    if form.validate_on_submit():
        plant.name = form.name.data
        plant.description = form.description.data
        plant.soil_texture = form.soil_texture.data
        plant.substrate = form.substrate.data
        plant.wiki_url = form.wiki_url.data
        plant.other_url = form.other_url.data
        if form.photo.data:
            plant.photo = upload_image(form.photo.data, 'images/plants')
        for value in values:
                value.min_value = getattr(form, value.indicator.lower()).min_value.data
                value.max_value = getattr(form, value.indicator.lower()).max_value.data
        db.session.commit()
        flash(f'Congratulations, Plant {plant.name} updated secessefuly!', 'success')
        return redirect(url_for('pyflora.view_plant', plant_id=plant_id))
    elif request.method == 'GET':
        form.name.data = plant.name
        form.description.data = plant.description
        form.soil_texture.data = plant.soil_texture
        form.substrate.data = plant.substrate
        form.wiki_url.data = plant.wiki_url
        form.other_url.data = plant.other_url
        for value in values:
            getattr(form, value.indicator.lower()).min_value.data = value.min_value
            getattr(form, value.indicator.lower()).max_value.data = value.max_value
    return render_template('pyflora/plant_new.html', title='Update PyPlant', form=form)

@bp.route('/plant/<plant_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    name = plant.name
    try:
        os.remove(os.path.join(current_app.config['UPLOADS_DEFAULT_DEST'], f'images/plants/{plant.photo}'))
    except:
        pass
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
    form = EmptyForm()
    pot = Pot.query.get(pot_id)
    plant = pot.plant
    values = plant.values.all()
    fig_line = PlotlyLine(pot).config()
    # fig_line = PLine(pot).config()
    line_graphJSON = json.dumps(fig_line, cls=plotly.utils.PlotlyJSONEncoder)
    fig_histo = PlotlyHisto(pot).config()
    histo_graphJSON = json.dumps(fig_histo, cls=plotly.utils.PlotlyJSONEncoder)
    fig_pie = PlotlyPie(pot).config()
    pie_graphJSON = json.dumps(fig_pie, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template(
        'pyflora/pot_view.html',
        title=pot.name,
        pot=pot,
        plant=plant,
        values=values,
        form=form,
        line_graphJSON=line_graphJSON,
        histo_graphJSON=histo_graphJSON,
        pie_graphJSON=pie_graphJSON
    )

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
        pot.owner=current_user
        pot.plant=plant
        db.session.add(pot)
        db.session.flush()
        for measure in current_app.config['MEASURES']:
            sensor = Sensor()
            sensor.indicator=measure
            sensor.pot=pot
            db.session.add(sensor)
        db.session.commit()
        flash(f'Congratulations, Pot {pot.name} added secessefuly!', 'success')
        return redirect(url_for('pyflora.list_pot'))
    return render_template('pyflora/pot_new.html', title='Add PyPot', form=form)


@bp.route('/pot/<pot_id>/update', methods=['GET', 'POST'])
@login_required
def update_pot(pot_id):
    pot = Pot.query.get_or_404(pot_id)
    sensors = pot.sensors.all()
    plants = Plant.query.all()
    plant_list = [(i.id, i.name) for i in plants]
    form = PotForm(pot.name)
    form.plant.choices = plant_list
    if form.validate_on_submit():
        plant = Plant.query.get(form.plant.data)
        pot.name=form.name.data
        pot.description=form.description.data
        pot.plant=plant
        db.session.flush()
        for sensor in sensors:
            sensor.active=getattr(form, sensor.indicator.lower()).data
        db.session.commit()
        flash(f'Congratulations, Pot {pot.name} updated secessefuly!', 'success')
        return redirect(url_for('pyflora.view_pot', pot_id=pot_id))
    elif request.method == 'GET':
        form.name.data = pot.name
        form.description.data = pot.description
        form.plant.data = pot.plant_id
        db.session.flush()
        for sensor in sensors:
            getattr(form, sensor.indicator.lower()).data=sensor.active
    return render_template('pyflora/pot_update.html', title='Update PyPot', form=form)


@bp.route('/pot/<pot_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_pot(pot_id):
    pot = Pot.query.get_or_404(pot_id)
    name = pot.name
    db.session.delete(pot)
    db.session.commit()
    flash(f'Congratulations, Pot {name} deleted secessefuly!', 'success')
    return redirect(url_for('pyflora.list_pot'))


@bp.route('/pot/<pot_id>/sync', methods=['POST'])
@login_required
def sync_pot(pot_id):
    pot = Pot.query.get(pot_id)
    SensorSim(pot).generate()
    return redirect(url_for('pyflora.view_pot', pot_id=pot_id))