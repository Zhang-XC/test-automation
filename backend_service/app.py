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


def get_authorized_token():
    token = request.headers.get("Authorization")
    if token in TOKENS:
        return token
    return None


@api.route('/login', methods=['POST'])
def login():
    username = flask.request.form.get('user_name')
    password = flask.request.form.get('passwd')
    if USERS.get(username) == password:
        token = uuid.uuid4()
        TOKENS[token] = username
        return jsonify({"token": token})
    else:
        return jsonify({"error": "Bad credentials"})
    

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
    if pid is not None and pid in PRODUCTS:
        CART.setdefault(token, []).append(PRODUCTS[pid])
        return jsonify({"message": "Added to cart"})
    return jsonify({"error": "Product not found"})


@api.route('/checkout', methods=['POST'])
def checkout():
    token = get_authorized_token()
    if token is None:
        return jsonify({"error": "Unauthorized"})
    total = sum(item["price"] for item in CART[token])
    CART[token] = []
    return jsonify({"message": "Checkout successful", "total": total})


if __name__ == "__main__":
    api.run(debug=True)