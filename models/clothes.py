from database import database as db


class Clothes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    min_temp = db.Column(db.Integer, nullable=False, default=-1000)
    max_temp = db.Column(db.Integer, nullable=False, default=1000)
    when_rain = db.Column(db.Boolean, default=False)
    when_snow = db.Column(db.Boolean, default=False)
    when_wind = db.Column(db.Boolean, default=False)
    is_accessoire = db.Column(db.Boolean, default=False)
