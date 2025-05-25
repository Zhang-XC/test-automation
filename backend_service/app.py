import os
import sys
import json
import uuid
import random

import flask

from flask import jsonify, make_response, request
from flask_jwt_extended import (
    create_access_token,
    JWTManager,
    jwt_required,
    set_access_cookies,
    get_jwt_identity,
)


app = flask.Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)


# Mock databases
USERS = {
    'testuser': {"user_id": "u123", "password": 'password123'}
}
PRODUCTS = {
    "1": {"name": "Laptop", "price": 1200},
    "2": {"name": "Headphones", "price": 150}
}
CART = {}
ORDERS = {}


@app.route('/auth/login', methods=['POST'])
def login():
    username = flask.request.form.get('user_name')
    password = flask.request.form.get('password')
    if username and password:
        user = USERS.get(username)
        if user and user["password"] == password:
            acc_token = create_access_token(identity=user["user_id"])
            response = jsonify({"message": "Login successful"})
            set_access_cookies(response, acc_token)
            return response
        else:
            return jsonify({"error": "Invalid username or password"})
    else:
        return jsonify({"error": "Missing key parameters"})
    

@jwt_required(locations=['headers'])
@app.route('/auth/register', methods=['POST'])
def register_user():
    username = flask.request.form.get('user_name')
    password = flask.request.form.get('password')
    if username and password:
        if username in USERS:
            return jsonify({"error": "Username exists"})
        USERS[username] = {
            "user_id": str(uuid.uuid4()),
            "password": password
        }
        return jsonify({"message": "Successfully registered user"})
    else:
        return jsonify({"error": "Missing key parameters"})


@app.route('/products', methods=['GET'])
def view_products():
    return jsonify(PRODUCTS)


@app.route('/products/<product_id>', methods=['GET'])
def view_product(product_id):
    if product_id in PRODUCTS:
        return jsonify(PRODUCTS[product_id])
    else:
        return jsonify({"error": "Product not found"})


@jwt_required(locations=['headers'])
@app.route('/cart', methods=['GET'])
def view_cart():
    user_id = get_jwt_identity()
    return jsonify(CART.get(user_id, []))


@jwt_required(locations=['headers'])
@app.route('/cart', methods=['POST'])
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.get_json()
    product_id = data.get("product_id")
    if product_id is not None :
        if product_id in PRODUCTS:
            product_info = PRODUCTS[product_id].copy()
            product_info["product_id"] = product_id
            CART.setdefault(user_id, []).append(product_info)
            return jsonify({"message": "Added to cart"})
        else:
            return jsonify({"error": "Product not found"})
    else:
        return jsonify({"error": "Missing key parameter"})


@jwt_required(locations=['headers'])
@app.route('/cart/remove', methods=['POST'])
def remove_from_cart():
    user_id = get_jwt_identity()
    data = request.get_json()
    pid = data.get("product_id")
    for i, product in enumerate(CART.get(user_id, [])):
        if pid == product["product_id"]:
            CART[user_id].pop(i)
            return jsonify({"message": "Successfully removed product from cart"})
    return jsonify({"error": "Product not found"})


@jwt_required(locations=['headers'])
@app.route('/orders', methods=['GET'])
def view_orders():
    user_id = get_jwt_identity()
    return jsonify(ORDERS.get(user_id, []))


@jwt_required(locations=['headers'])
@app.route('/orders/<order_id>', methods=['GET'])
def view_order(order_id):
    user_id = get_jwt_identity()
    for order in ORDERS.get(user_id, []):
        if order_id == order["order_id"]:
            return jsonify(order)
    return jsonify({"error": "Order not found"})


@jwt_required(locations=['headers'])
@app.route('/checkout', methods=['POST'])
def checkout():
    user_id = get_jwt_identity()
    total = sum(item["price"] for item in CART.get(user_id, []))
    ORDERS.setdefault(user_id, []).append({
        "order_id": str(uuid.uuid4()),
        "cart": CART[user_id].copy(),
        "total": total
    })
    CART[user_id] = []
    return jsonify({"message": "Checkout successful", "total": total})


if __name__ == "__main__":
    app.run(debug=True)