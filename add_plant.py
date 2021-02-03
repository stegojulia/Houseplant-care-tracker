from flask import Flask, render_template, request, redirect, url_for
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
db = SQLAlchemy(app)

class NullableDateField(DateField):
    """Native WTForms DateField throws error for empty dates.
    Let's fix this so that we could have DateField nullable."""
    def process_formdata(self, valuelist):
        if valuelist:
            date_str = ' '.join(valuelist).strip()
            if date_str == '':
                self.data = None
                return
            try:
                self.data = datetime.date.strptime(date_str, self.format).date()
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Not a valid date value'))

class Houseplants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    houseplant_name = db.Column(db.String(45), nullable=False, unique = True)
    species = db.Column(db.String(45))
    family = db.Column(db.String(45))
    date_acquired = db.Column(db.Date)
    source = db.Column(db.String(45))

    def __repr__(self):
        return f"Houseplants('{self.id}', '{self.houseplant_name}', '{self.species}', '{self.family}', '{self.date_acquired}', '{self.source}'"

#class Waterings(db.Model):
#    watering_id = db.Column(db.Integer, primary_key=True)
#    plant_id = db.Column(db.Integer), db.ForeignKey('houseplants.id', nullable=False)

#db.drop_all()
db.create_all()


##form to add houseplants

class AddHouseplantForm(FlaskForm):
    houseplant_name = StringField('Houseplant name', validators=[Length(min=3, max=20, message='Houseplant name has to be between 3 and 20 characters'), DataRequired()])
    species = StringField('Species')
    family = StringField('Family')
    date_acquired = DateField('Date acquired (YYYY-MM-DD)',format='%Y-%m-%d')
    source = StringField('Source')
    submit = SubmitField('Add')


@app.route("/")

@app.route("/home")
def home():
    plants = Houseplants.query.all()
    return render_template('home.html', plants=plants)

@app.route("/add", methods=['GET', 'POST'])
def add():
    form = AddHouseplantForm()
    if form.is_submitted():
        plant = Houseplants(houseplant_name=form.houseplant_name.data, species=form.species.data, family=form.family.data, date_acquired =form.date_acquired.data, source=form.source.data)
        db.session.add(plant)
        db.session.commit()
        return redirect(url_for('home'))
    plants = Houseplants.query.all()
    return render_template('add.html', title='Add plant', form=form, plants=plants, legend = "Add a plant")

@app.route("/plant/<int:plant_id>")
def plant(plant_id):    
    plant = Houseplants.query.get_or_404(plant_id)
    return render_template('plant.html', title=plant.houseplant_name, plant=plant, plant_id = plant.id)

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
    db.session.delete(plant)
    db.session.commit()
    return redirect(url_for('home', plant_id = plant.id))

#@app.route("/plant/<int:plant_id>/water", methods=['POST'])
#def water_plant(plant_id):
#    watering = Waterings(plant_id=plant_id)
#    db.session.add(watering)
#    db.session.commit()
#    return redirect(url_for('home', plant_id = plant.id))

if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0')
