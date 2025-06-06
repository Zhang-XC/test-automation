import uuid
import sqlite3

import flask

from flask import jsonify, request, g
from flask_jwt_extended import (
    create_access_token,
    JWTManager,
    jwt_required,
    get_jwt_identity,
)
from bcrypt import hashpw, checkpw, gensalt
from common.database import get_db
from common.settings import URL_HOST


app = flask.Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)


@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/auth/login', methods=['POST'])
def login():
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    if not (username and password):
        return jsonify({"error": "Missing key parameters"}), 400
    
    password_hash = hashpw(password.encode(), gensalt())
    db = get_db()
    cur = db.execute("SELECT * FROM users WHERE username = ?", [username])
    user = cur.fetchone()
    if user and checkpw(user["password"].encode(), password_hash):
        acc_token = create_access_token(identity=str(user["user_id"]))
        response = jsonify({"message": "Login successful", "token": acc_token})
        return response, 200
    else:
        return jsonify({"error": "Invalid username or password"}), 400
    

@app.route('/users', methods=['POST'])
def register_user():
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    if not (username and password):
        return jsonify({"error": "Missing key parameters"}), 400
    
    password_hash = hashpw(password.encode(), gensalt())
    user_id = str(uuid.uuid4())
    try:
        db = get_db()
        db.execute(
            "INSERT INTO users (user_id, username, password) VALUES (?, ?, ?)", 
            [user_id, username, password_hash.decode()]
        )
        db.commit()
        return jsonify({"message": "Successfully registered user"}), 200
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username exists"}), 409


@app.route('/users/me', methods=['DELETE'])
@jwt_required(locations=['headers'])
def delete_user():
    user_id = get_jwt_identity()
    db = get_db()
    cur = db.execute(
        "DELETE FROM users WHERE user_id = ?",
        [user_id]
    )
    db.commit()
    if cur.rowcount == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "Successfully deleted user"}), 200


@app.route('/products', methods=['GET'])
def view_products():
    db = get_db()
    cur = db.execute("SELECT * FROM products")
    products = cur.fetchall()
    return jsonify([dict(product) for product in products]), 200


@app.route('/products/<product_id>', methods=['GET'])
def view_product(product_id):
    db = get_db()
    cur = db.execute("SELECT * FROM products WHERE product_id = ?", [product_id])
    product = cur.fetchone()
    if product:
        return jsonify(dict(product)), 200
    else:
        return jsonify({"error": "Product not found"}), 404


@app.route('/cart_items', methods=['GET'])
@jwt_required(locations=['headers'])
def view_cart():
    user_id = get_jwt_identity()
    db = get_db()
    cur = db.execute("SELECT * FROM cart_items WHERE user_id = ?", [user_id])
    cart_items = cur.fetchall()
    return jsonify([dict(item) for item in cart_items]), 200


@app.route('/cart_items', methods=['POST'])
@jwt_required(locations=['headers'])
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.get_json()
    product_id = data.get("product_id")
    if not product_id:
        return jsonify({"error": "Missing key parameter"}), 400
    
    db = get_db()
    cur = db.execute(
        "SELECT * FROM cart_items WHERE user_id = ? AND product_id = ?",
        [user_id, product_id]
    )
    cart_item = cur.fetchone()

    if cart_item:
        db.execute(
            "UPDATE cart_items SET quantity = quantity + 1 WHERE user_id = ? AND product_id = ?",
            [user_id, product_id]
        )
    else:
        try:
            db.execute(
                "INSERT INTO cart_items (user_id, product_id, quantity) VALUES (?, ?, ?)",
                [user_id, product_id, 1]
            )
        except sqlite3.IntegrityError:
            return jsonify({"error": "Invalid user_id or product_id"}), 400
    db.commit()
    return jsonify({"message": "Successfully added item to cart"}), 200


@app.route('/cart_items/<product_id>', methods=['DELETE'])
@jwt_required(locations=['headers'])
def remove_from_cart(product_id):
    user_id = get_jwt_identity()
    
    db = get_db()
    cur = db.execute(
        "SELECT quantity FROM cart_items WHERE user_id = ? AND product_id = ?",
        [user_id, product_id]
    )
    row = cur.fetchone()
    if not row:
        return jsonify({"error": "Item not found in cart"}), 404
    
    quantity = row["quantity"]
    if quantity > 1:
        db.execute(
            "UPDATE cart_items SET quantity = quantity - 1 WHERE user_id = ? AND product_id = ?",
            [user_id, product_id]
        )
    else:
        db.execute(
            "DELETE FROM cart_items WHERE user_id = ? AND product_id = ?",
            [user_id, product_id]
        )
    db.commit()
    return jsonify({"message": "Successfully removed product from cart"}), 200


@app.route('/orders', methods=['GET'])
@jwt_required(locations=['headers'])
def view_orders():
    user_id = get_jwt_identity()
    db = get_db()
    cur = db.execute("SELECT * FROM orders WHERE user_id = ?", [user_id])
    orders = cur.fetchall()
    return jsonify([dict(order) for order in orders]), 200


@app.route('/orders', methods=['POST'])
@jwt_required(locations=['headers'])
def checkout():
    user_id = get_jwt_identity()
    db = get_db()
    query = """
    SELECT C.product_id, C.quantity, P.price
    FROM cart_items AS C
    JOIN products AS P ON C.product_id = P.product_id
    WHERE C.user_id = ?
    """
    cur = db.execute(query, [user_id])
    cart_items = cur.fetchall()

    order_total = 0
    order_id = str(uuid.uuid4())
    for item in cart_items:
        product_id = item["product_id"]
        price = item["price"]
        quantity = item["quantity"]
        db.execute(
            "DELETE FROM cart_items WHERE user_id = ? AND product_id = ?",
            [user_id, product_id]
        )
        db.execute(
            "INSERT INTO orders (order_id, user_id, product_id, quantity, total_price) VALUES (?, ?, ?, ?, ?)",
            [order_id, user_id, product_id, quantity, price * quantity]
        )
        order_total += price * quantity
    db.commit()
    return jsonify({"message": "Checkout successful", "total": order_total}), 200


if __name__ == "__main__":
    host, port = URL_HOST.replace("http://", "").replace("https://", "").split(":")
    app.run(host=host, port=int(port), debug=True)