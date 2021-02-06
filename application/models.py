from application import db

class Houseplants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    houseplant_name = db.Column(db.String(45), nullable=False)
    species = db.Column(db.String(45))
    family = db.Column(db.String(45))
    date_acquired = db.Column(db.Date)
    source = db.Column(db.String(45))
    waterings = db.relationship('Waterings', backref='houseplants')

class Waterings(db.Model):
    watering_id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('houseplants.id'), nullable=False)
    date = db.Column(db.Date)
