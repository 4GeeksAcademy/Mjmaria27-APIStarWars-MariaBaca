import os
from flask import Flask, jsonify, request, redirect
from flask_migrate import Migrate
from models import db, User, People, Planet, Favorite
from admin_panel import setup_admin


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///starwars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
Migrate(app, db)
setup_admin(app)  # ✅ Activa el panel de administración

# --- RUTAS DE LA API ---

@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    result = [{"id": p.id, "name": p.name, "gender": p.gender} for p in people]
    return jsonify(result), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_person(people_id):
    person = People.query.get(people_id)
    if person:
        return jsonify({"id": person.id, "name": person.name, "gender": person.gender}), 200
    return jsonify({"error": "Not found"}), 404

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    result = [{"id": p.id, "name": p.name, "climate": p.climate} for p in planets]
    return jsonify(result), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        return jsonify({"id": planet.id, "name": planet.name, "climate": planet.climate}), 200
    return jsonify({"error": "Not found"}), 404

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = [{"id": u.id, "email": u.email} for u in users]
    return jsonify(result), 200

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = 1  # Simulación: sin login
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    result = []
    for fav in favorites:
        if fav.planet_id:
            result.append({"type": "planet", "id": fav.planet_id})
        if fav.people_id:
            result.append({"type": "people", "id": fav.people_id})
    return jsonify(result), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_planet_favorite(planet_id):
    user_id = 1
    fav = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify({"message": "Planet favorite added"}), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_people_favorite(people_id):
    user_id = 1
    fav = Favorite(user_id=user_id, people_id=people_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify({"message": "People favorite added"}), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet_favorite(planet_id):
    user_id = 1
    fav = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
        return jsonify({"message": "Planet favorite removed"}), 200
    return jsonify({"error": "Not found"}), 404

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_people_favorite(people_id):
    user_id = 1
    fav = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
        return jsonify({"message": "People favorite removed"}), 200
    return jsonify({"error": "Not found"}), 404

# --- REDIRECCIÓN DE INICIO AL ADMIN ---
@app.route('/')
def home():
    return redirect('/admin')  # ✅ Redirige automáticamente al panel de administración
