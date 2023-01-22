from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    characterID = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True, nullable = False)
    eyed_color = db.Column(db.String(80), unique = False, nullable = False)
    birth_year = db.Column(db.String(80), unique = False, nullable = False)
    height = db.Column(db.Integer, unique = False, nullable = False)
    mass = db.Column(db.Integer, unique = False, nullable = False)
    url = db.Column(db.String(200), unique = False, nullable = False)
    homeworld = db.Column(db.String(200), unique = False, nullable = False)


    def serialize(self):
        return {
            'characterID' : self.CharacterID,
            'name' : self.name,
            'eyed_color' : self.eyed_color,
            'birth_year' : self.birth_year,
            'height' : self.height,
            'mass' : self.mass,
            'url' : self.url,
            'homeworld' : self.homeworld
        }    

class Planet(db.Model):
    planetID = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True, nullable = False)
    rotated_period  = db.Column(db.String(80), unique = False, nullable = False)
    diameter = db.Column(db.Integer, unique = False, nullable = False)
    climate = db.Column(db.String(80), unique = False, nullable = False)
    orbital_period = db.Column(db.Integer, unique = False, nullable = False)
    url = db.Column(db.String(200), unique = False, nullable = False)
    
    def serialize(self):
        return {
            'planetID' : self.planetID,
            'name': self.name,
            'rotated_period' : self.rotated_period,
            'diameter': self.diameter,
            'climate': self.climate,
            'orbital_period': self.orbital_period,
            'url': self.url
        }   
    
planet_favourites = db.Table('planet_favourites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('planet_id', db.Integer, db.ForeignKey('planet.planetID'), primary_key=True)
)

people_favourites = db.Table('people_favourites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True),
    db.Column('people_id', db.Integer, db.ForeignKey('people.characterID'), nullable=False, primary_key=True)
)