from app import app, db
from bson import ObjectId

from flask import (request, abort)
import json


@app.route('/users/authenticate', methods=['POST'])
def login():
    user = {
        "login": request.json['login'],
        "password": request.json['password']
    }
    has_user = db['users'].find_one({"login": user["login"]})
    if not has_user:
        abort(404)
    elif user['password'] != has_user['password']:
        abort(400)
    else:
        has_user['_id'] = str(has_user['_id'])
        del has_user['password']
        return encode_json(has_user)


@app.route('/users', methods=['POST'])
def create_user():
    user = {
        "login": request.json['login'],
        "name": request.json['name'],
        "password": request.json['password']
    }
    has_user = db['users'].find_one({"login": user["login"]})
    if not has_user:
        db['users'].insert(user)
        user['_id'] = str(user['_id'])
        return encode_json(user)
    else:
        abort(400)


@app.route('/products', methods=['POST'])
def create_product():
    product = {
        "code": request.json['code'],
        "name": request.json['name'],
        "description": request.json['description'],
        "price": request.json['price'],
        "grid": []
    }
    grid = request.json['grid']
    for item in grid:
        product['grid'].append({
            "color": item['color'],
            "size": item['size']
        })
    db['products'].insert(product)
    product['_id'] = str(product['_id'])
    return encode_json(product)


@app.route('/products', methods=['GET'])
def find_products():
    products = db['products'].find()
    products_find = []
    for item in products:
        product = {
            "code": item['code'],
            "name": item['name'],
            "description": item['description'],
            "price": item['price'],
            "grid": []
        }
        grids = item['grid']
        for grid in grids:
            product['grid'].append({
                "color": grid['color'],
                "size": grid['size']
            })
        product['_id'] = str(item['_id'])
        products_find.append(product)

    return encode_json(products_find)


@app.route('/products/<product_id>', methods=['GET'])
def find_product_by_id(product_id):
    item = db['products'].find_one({"_id": ObjectId(product_id)})
    if item:
        product = {
            "code": item['code'],
            "name": item['name'],
            "description": item['description'],
            "price": item['price'],
            "grid": []
        }
        grids = item['grid']
        for grid in grids:
            product['grid'].append({
                "color": grid['color'],
                "size": grid['size']
            })
        product['_id'] = str(item['_id'])

        return encode_json(product)
    else:
        abort(404)


def encode_json(value):
    return json.dumps(value, ensure_ascii=False).encode('utf8')
