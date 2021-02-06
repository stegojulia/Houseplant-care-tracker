from application import app, db
from application.models import Houseplants, Waterings

from flask import Flask, render_template, request, redirect, url_for

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired, Length

import datetime

class AddHouseplantForm(FlaskForm):
    houseplant_name = StringField('Houseplant name', validators=[Length(min=3, max=20, message='Houseplant name has to be between 3 and 20 characters'), DataRequired()])
    species = StringField('Species')
    family = StringField('Family')
    date_acquired = DateField('Date acquired (YYYY-MM-DD)',format='%Y-%m-%d')
    source = StringField('Source')
    submit = SubmitField('Add')

class WaterPlantForm(FlaskForm):
    watering_date = DateField('Watering date (YYYY-MM-DD)', format='%Y-%m-%d', default=datetime.datetime.now())
    submit = SubmitField('Water')


@app.route("/")
def home():
    plants = Houseplants.query.all()
    return render_template('home.html', plants=plants)

@app.route("/add", methods=['GET', 'POST'])
def add():
    form = AddHouseplantForm()
    if form.validate_on_submit() or (len(form.errors.items())==1 and [field for field,error in form.errors.items()][0]=='date_acquired'):
        plant = Houseplants(
            houseplant_name=form.houseplant_name.data, species=form.species.data, family=form.family.data, date_acquired =form.date_acquired.data, source=form.source.data
            )
        db.session.add(plant)
        db.session.commit()
        return redirect(url_for('home'))
    plants = Houseplants.query.all()
    return render_template('add.html', title='Add plant', form=form, plants=plants, legend = "Add a plant")

@app.route("/plant/<int:plant_id>")
def plant(plant_id):    
    plant = Houseplants.query.get_or_404(plant_id)
    try:
        all_waterings = Waterings.query.filter_by(plant_id=plant_id).order_by(Waterings.date)
        latest_watering = all_waterings[-1]
    except:
        latest_watering = 'not watered'  
    return render_template('plant.html', title=plant.houseplant_name, plant=plant, plant_id = plant.id, latest_watering=latest_watering)

@app.route("/plant/<int:plant_id>/update", methods=['GET', 'POST'])
def update_plant(plant_id):
    plant = Houseplants.query.get_or_404(plant_id)
    form = AddHouseplantForm()
    if form.is_submitted():
        plant.houseplant_name= form.houseplant_name.data
        plant.species = form.species.data
        plant.family = form.family.data
        plant.date_acquired = form.date_acquired.data
        plant.source = form.source.data
        db.session.commit()
        return redirect(url_for('plant', plant_id=plant.id))
    form.houseplant_name.data = plant.houseplant_name
    form.species.data = plant.species
    form.family.data = plant.family
    form.date_acquired.data = plant.date_acquired
    form.source.data = plant.source
    return render_template('add.html', title='Update plant', form=form, legend="Update plant")

@app.route("/plant/<int:plant_id>/delete", methods=['POST'])
def delete_plant(plant_id):
    plant = Houseplants.query.get_or_404(plant_id)
    all_waterings = Waterings.query.filter_by(plant_id=plant_id)
    for water in all_waterings:
        db.session.delete(water)
    db.session.delete(plant)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/plant/<int:plant_id>/care", methods=['GET', 'POST'])
def care(plant_id):
    plant = Houseplants.query.get_or_404(plant_id)
    all_waterings = Waterings.query.filter_by(plant_id=plant_id).order_by(Waterings.date.desc())
    form = WaterPlantForm()
    if form.validate_on_submit():
        new_watering = Waterings(plant_id=plant_id, date=form.watering_date.data)
        db.session.add(new_watering)
        db.session.commit()
    return render_template('care.html', all_waterings=all_waterings, plant=plant, form=form, legend="Care sheet")

@app.route("/plant/<int:watering_id>/delete", methods=['GET','POST'])
def delete_care(watering_id):
    watering = Waterings.query.get_or_404(watering_id)
    db.session.delete(watering)
    db.session.commit()
    return redirect(url_for('care', plant_id = watering.plant_id))