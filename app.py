from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy, Model
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields

app = Flask(__name__)

#set the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sarahj@localhost/recipe'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

#initialize the database
db = SQLAlchemy(app)

#initialize marshmallow
ma = Marshmallow(app)

#product model
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))

    def __init__(self, name, description):
        self.name = name
        self.description = description


@app.route('/recipe', methods=['GET'])
def get_all_recipes():
    all_recipes = Recipe.query.all()
    result = Recipe.Schema.dump(all_recipes)
    return jsonify(result.data)

@app.route('/recipe/<int:id>', methods=['GET'])
def get_recipe():
    recipe = Recipe.query.get(id)
    return recipe_schema.jsonify(recipe)

@app.route('/recipe', methods=['POST'])
def add_recipe():
    name = request.json['name']
    description = request.json['description']

    new_recipe = Recipe(name, description)

    db.session.add(new_recipe)
    db.session.commit()

    return recipe_schema.jsonify(new_recipe)

@app.route('/recipe/<id>', methods=['PUT'])
def update_recipe(id):
    recipe = Recipe.query.get(id)

    name = request.json['name']
    description = request.json['description']

    recipe.name = name
    recipe.description= description

    db.session.commit()

    return recipe_schema.jsonify(recipe)

@app.route('/recipe/<id>', methods=['DELETE'])
def delete_recipe():
    recipe = Recipe.query.get(id)
    db.session.delete(recipe)
    db.session.commit()
    return '', 204

class RecipeSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()

if __name__ == "__main__":
    app.run(debug=True)