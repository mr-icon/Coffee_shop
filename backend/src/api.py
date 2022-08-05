import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()

# ROUTES
@app.route('/drinks')
def get_drinks():
    try:
        drinks = Drink.query.all()

        return jsonify({
            "success": True,
            "drinks": [drink.short() for drink in drinks]
        })
    except:
        abort(404)
    


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(f):
    try:
        drinks = Drink.query.all()

        return jsonify({
            "success": True,
            "drinks": [drink.long() for drink in drinks]
        })
    except:
        abort(404)


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drinks(f):
    data = request.get_json()
    try:
        new_title = data.get("title", None)
        new_recipe = data.get("recipe", None)



        drinks = Drink(title=title, recipe=recipe)
        drinks.insert()

        return jsonify({
            "success": True,
            "drinks": [drinks.long()]
        })
    except:
        abort(422)



@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drinks(f, id):
    try:
        request_params = request.get_json()

        update = request_params
        update = {
            "title": title,
            "recipe": recipe,
        }

        return jsonify({
                "success": True,
                "drinks": [drinks.long()]
            })
    except:
        abort(404) 


@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(f, id):
    try:
        drinks = Drink.query.get(id)
        response['id'] = drinks.id

        db.session.delete(drinks)
        db.session.commit()

        return jsonify({
            "success": True,
            "delete": id
        })
    except:
        abort(404)

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422



@app.errorhandler(404)
def not_found(error):
            return jsonify({
                    'success': False,
                    'error': 404,
                    'message': 'Not Found'
            }), 404


@app.errorhandler(AuthError)
def auth_error(error):
    response = jsonify (error.error)
    response.status_code = error.status_code
    return response
