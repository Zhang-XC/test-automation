import os
import sys
import json
import uuid
import random

import flask

from flask import jsonify, make_response, request


api = flask.Flask(__name__)

# Mock databases
USERS = {
    'testuser': 'password123'
}
TOKENS = {}
PRODUCTS = {
    "1": {"name": "Laptop", "price": 1200},
    "2": {"name": "Headphones", "price": 150}
}
CART = {}
ORDERS = {}


def get_authorized_token():
    token = request.headers.get("Authorization")
    if token in TOKENS:
        return token
    return None


@api.route('/auth/login', methods=['POST'])
def login():
    username = flask.request.form.get('user_name')
    password = flask.request.form.get('passwd')
    if username and password:
        if USERS.get(username) == password:
            token = uuid.uuid4()
            TOKENS[token] = username
            return jsonify({"token": token})
        else:
            return jsonify({"error": "Bad credentials"})
    else:
        return jsonify({"error": "Missing key parameters"})
    

@api.route('/auth/register', methods=['POST'])
def register_user():
    username = flask.request.form.get('user_name')
    password = flask.request.form.get('passwd')
    if username and password:
        if username in USERS:
            return jsonify({"error": "Username exists"})
        USERS[username] = password
        return jsonify({"message": "Successfully registered user"})
    else:
        return jsonify({"error": "Missing key parameters"})
    

@api.route('/auth/logout', methods=['POST'])
def logout():
    token = get_authorized_token()
    if token is None:
        return jsonify({"error": "Unauthorized"})
    TOKENS.pop(token)
    return jsonify({"message": "Successfully logged out"})


@api.route('/products', methods=['GET'])
def view_products():
    return jsonify(PRODUCTS)


@api.route('/products/<product_id>', methods=['GET'])
def view_product(product_id):
    if product_id in PRODUCTS:
        return jsonify(PRODUCTS[product_id])
    else:
        return jsonify({"error": "Product not found"})


@api.route('/cart', methods=['GET'])
def view_cart():
    token = get_authorized_token()
    if token is None:
        return jsonify({"error": "Unauthorized"})
    return jsonify(CART.get(token, []))


@api.route('/cart', methods=['POST'])
def add_to_cart():
    token = get_authorized_token()
    if token is None:
        return jsonify({"error": "Unauthorized"})
    data = request.get_json()
    pid = data.get("product_id")
    if pid is not None :
        if pid in PRODUCTS:
            product_info = PRODUCTS[pid].copy()
            product_info["product_id"] = pid
            CART.setdefault(token, []).append(product_info)
            return jsonify({"message": "Added to cart"})
        else:
            return jsonify({"error": "Product not found"})
    else:
        return jsonify({"error": "Missing key parameter"})


@api.route('/cart/remove', methods=['POST'])
def remove_from_cart():
    token = get_authorized_token()
    if token is None:
        return jsonify({"error": "Unauthorized"})
    data = request.get_json()
    pid = data.get("product_id")
    for i, product in enumerate(CART[token]):
        if pid == product["product_id"]:
            CART[token].pop(i)
            return jsonify({"message": "Successfully removed product from cart"})
    return jsonify({"error": "Product not found"})


@api.route('/orders', methods=['GET'])
def view_orders():
    token = get_authorized_token()
    if token is None:
        return jsonify({"error": "Unauthorized"})
    return jsonify(ORDERS.get(token, {}))


@api.route('/orders/<order_id>', methods=['GET'])
def view_order(order_id):
    token = get_authorized_token()
    if token is None:
        return jsonify({"error": "Unauthorized"})
    for oid, order in ORDERS.get(token, {}):
        if order_id == oid:
            return jsonify({order})
    return jsonify({"error": "Order not found"})


@api.route('/checkout', methods=['POST'])
def checkout():
    token = get_authorized_token()
    if token is None:
        return jsonify({"error": "Unauthorized"})
    total = sum(item["price"] for item in CART[token])
    ORDERS[token] = {
        "order_id": uuid.uuid4(),
        "cart": CART[token],
        "total": total
    }
    CART[token] = []
    return jsonify({"message": "Checkout successful", "total": total})


if __name__ == "__main__":
    api.run(debug=True)