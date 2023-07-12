"""
https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/
"""

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Create the extension
db = SQLAlchemy()

# Create the app
app = Flask(__name__)

# Create a SQLite Database called data.db in the same directory
# relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

# Initialize the app with the extension
db.init_app(app)

# Define Models
class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"

# Call SQLAlchemy.create_all() to create the table schema in the database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return "Hello!"

@app.route("/drinks")
def get_drinks():
    drinks = Drink.query.all()
    output = []
    for drink in drinks:
        drink_data = {"name": drink.name, "description": drink.description}
        output.append(drink_data)
    
    return {"drinks": output}, 200

@app.route("/drinks/<id>")
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    return {"name": drink.name, "description": drink.description}, 200

@app.route("/drinks", methods=["POST"])
def add_drink():
    drink = Drink(name=request.json["name"], description=request.json["description"])
    db.session.add(drink)
    db.session.commit()
    return {"id": drink.id}, 201

@app.route("/drinks/<id>", methods=["DELETE"])
def delete_drink(id):
    """ drink = Drink.query.get(id)
    if drink is None:
        return {"error": "Not Found"}, 404
    db.session.delete(drink)
    db.session.commit()
    return {"id": drink.id}, 200 """
    drink = Drink.query.get_or_404(id)
    # This way, we keep the 404 HTML Error page if the id does not exist
    #print(drink)

    # If the id does not exist in the DB, the drink variable will be 'None'
    # and it does not matter if it is passed on to db.session.delete(drink).
    # It will attempt to delete a None object, which does nothing.
    db.session.delete(drink)
    db.session.commit()
    return {"id": drink.id}, 200

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=81)