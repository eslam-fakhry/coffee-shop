import os
import sys
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink, db
from .auth.auth import AuthError, requires_auth
from .errors import (
    BadRequestError,
    MissingFieldError,
    DuplicatedFieldError,
    HttpError)


app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

# ROUTES


@app.route("/drinks")
def get_drinks():
    drinks = Drink.query.all()
    formatted_drinks = [d.short() for d in drinks]

    return jsonify({
        "success": True,
        "drinks": formatted_drinks
    })


@app.route("/drinks-detail")
@requires_auth(permission="get:drinks-detail")
def get_drinks_datail():
    drinks = Drink.query.all()
    formatted_drinks = [d.long() for d in drinks]

    return jsonify({
        "success": True,
        "drinks": formatted_drinks
    })


def get_validated_drink():
    data = request.get_json()
    if not data:
        raise BadRequestError("No data was provided")

    title = data.get('title', None)
    if not title:
        raise MissingFieldError('title')

    recipe = data.get('recipe', None)
    if not recipe:
        raise MissingFieldError('recipe')

    if not recipe.get('name', None):
        raise MissingFieldError('recipe.name')

    if not recipe.get('color', None):
        raise MissingFieldError('recipe.color')

    if not recipe.get('parts', None):
        raise MissingFieldError('recipe.parts')
    return (title, recipe)


@app.route("/drinks", methods=["POST"])
@requires_auth(permission="post:drinks")
def add_drink():
    error = False
    formatted_drink = None

    title, recipe = get_validated_drink()
    recipe_json = json.dumps([recipe])
    drink = Drink(
        title=title,
        recipe=recipe_json
    )
    try:
        drink.insert()
        formatted_drink = drink.long()
    except exc.IntegrityError:
        raise DuplicatedFieldError('title', title)
    except Exception:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        abort(422)

    drinks = [formatted_drink] if formatted_drink else []

    return jsonify({
        "success": True,
        "drinks": drinks
    })


@app.route("/drinks/<int:id>", methods=["PATCH"])
@requires_auth(permission="patch:drinks")
def update_drink(id):
    error = False
    formatted_drink = None

    data = request.get_json()
    if not data:
        raise BadRequestError("No data was provided")

    title = data.get('title', None)
    recipe = data.get('recipe', None)

    if not title and not recipe:
        raise MissingFieldError('recipe/title')

    drink = Drink.query.get_or_404(id)

    if title:
        drink.title = title

    if recipe:
        drink.recipe = json.dumps(recipe)

    try:
        drink.update()
        formatted_drink = drink.long()
    except exc.IntegrityError:
        raise DuplicatedFieldError('title', title)
    except Exception:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        abort(422)

    return jsonify({
        "success": True,
        "drinks": [formatted_drink]
    })


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


# Error Handling


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
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(AuthError)
def handle_auth_error(err):
    return jsonify({
        "success": False,
        "error": err.status_code,
        "message": err.error['description']
    }), err.status_code


@app.errorhandler(HttpError)
def handle_auth_error(err):
    return jsonify({
        "success": False,
        "error": err.status_code,
        "message": err.message
    }), err.status_code
