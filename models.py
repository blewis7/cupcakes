"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from sqlalchemy.sql.schema import ForeignKey

db = SQLAlchemy()

DEFAULT_CUPCAKE_IMAGE =  'https://tinyurl.com/demo-cupcake'


class Cupcake(db.Model):
    '''Insert type of cupcake'''

    __tablename__ = "cupcakes"

    id = db.Column(db.Integer, primary_key=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, default=DEFAULT_CUPCAKE_IMAGE)


def connect_db(app):
    '''Connect to database.'''

    db.app = app
    db.init_app(app)
