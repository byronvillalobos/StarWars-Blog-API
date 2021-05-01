from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    fullName = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    Favorites = db.relationship('Favorites', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.fullName

    def serialize(self):
        return {
            "id": self.id,
            "fullName": self.fullName,
            "email": self.email,
            "Favorites": list(map(lambda x: x.serialize(), self.Favorites))
            # do not serialize the password, its a security breach
        }


class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    height= db.Column(db.String(50))
    mass = db.Column(db.String(50))
    skin_color = db.Column(db.String(50))
    hair_color = db.Column(db.String(50))
    eye_color = db.Column(db.String(50))
    birth_year = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    photoUrl = db.Column(db.String(500))
    Favorites = db.relationship('Favorites', lazy=True)
    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass" : self.mass,
            "skin_color" : self.skin_color,
            "hair_color" : self.hair_color,
            "eye_color" : self.eye_color,
            "birth_year" : self.birth_year,
            "gender" : self.gender,
            "photoUrl" : self.photoUrl,
            "Favorites": list(map(lambda x: x.serialize(), self.Favorites))
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    population= db.Column(db.String(50))
    terrain = db.Column(db.String(50))
    climate = db.Column(db.String(50))
    gravity = db.Column(db.String(50))
    # eye_color = db.Column(db.String(50))
    surface_water = db.Column(db.String(50))
    orbital_period = db.Column(db.String(50))
    rotation_period = db.Column(db.String(50))
    photoUrl = db.Column(db.String(500), nullable=False)
    Favorites = db.relationship('Favorites', lazy=True)
    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "terrain" : self.terrain,
            "climate" : self.climate,
            "gravity" : self.gravity,
            # "eye_color" : self.eye_color,
            "surface_water" : self.surface_water,
            "orbital_period" : self.orbital_period,
            "photoUrl" : self.photoUrl,
            "Favorites": list(map(lambda x: x.serialize(), self.Favorites))
            # do not serialize the password, its a security breach
        }

class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    model= db.Column(db.String(50))
    vehicle_class = db.Column(db.String(50))
    passengers = db.Column(db.String(50))
    # photoUrl = db.Column(db.String(500), nullable=False)
    Favorites = db.relationship('Favorites', lazy=True)
    def __repr__(self):
        return '<Vehicles %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "vehicle_class" : self.vehicle_class,
            "passengers" : self.passengers,
            # "photoUrl" : self.photoUrl,
            "Favorites": list(map(lambda x: x.serialize(), self.Favorites))
            # do not serialize the password, its a security breach
        }

class Favorites(db.Model):
    __tablename__ = 'Favorites'
    id = db.Column(db.Integer, primary_key=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planets_id = db.Column(db.Integer,db.ForeignKey("planets.id"))
    people_id = db.Column(db.Integer,db.ForeignKey("people.id"))
    vehicles_id = db.Column(db.Integer,db.ForeignKey("vehicles.id"))

    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "nombre" : self.nombre,
            "user_id" : self.id_user,
            "planets_id" : self.planets_id,
            "people_id" : self.people_id,
            "vehicles_id" : self.vehicles_id,

            # do not serialize the password, its a security breach
        }