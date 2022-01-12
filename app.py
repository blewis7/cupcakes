"""Flask app for Cupcakes"""

from flask import Flask, request, redirect, render_template, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SECRET_KEY'] = 'brockisgood'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
# db.drop_all()
# db.create_all()


def serialize_cupcake(cupcake):
    '''Serialize a cupcake obj to a dictionary'''

    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }


@app.route('/')
def root():
    '''Homepage'''

    return render_template('index.html')


@app.route('/api/cupcakes')
def cupcake_index():
    '''Show a list of the cupcakes within the database'''

    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(c) for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.route('/api/cupcakes/<int:cupcake_id>')
def show_cupcake(cupcake_id):
    '''show single cupcake data'''

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)


@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    '''create a new cupcake'''

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"] or None

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcake(new_cupcake)

    return (jsonify(cupcake=serialized), 201)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def update_cupcake(cupcake_id):
    '''update cupcake in database'''

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json["flavor"]
    cupcake.size = request.json["size"]
    cupcake.rating = request.json["rating"]
    cupcake.image = request.json["image"]

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=serialize_cupcake(cupcake))


@app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    '''remove cupcake in database'''

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")
