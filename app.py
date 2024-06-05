from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from models import db, User, PlayerProperties
from utils import hash_password, verify_password, create_token

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

db.init_app(app)
jwt = JWTManager(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "User already exists"}), 409
    
    new_user = User(username=username, password=hash_password(password))
    new_properties = PlayerProperties(user=new_user)
    db.session.add(new_user)
    db.session.add(new_properties)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not verify_password(user.password, password):
        return jsonify({"message": "Invalid credentials"}), 401
    
    access_token = create_token(identity=username)
    return jsonify(access_token=access_token), 200

@app.route('/properties', methods=['GET', 'PUT'])
@jwt_required()
def properties():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    
    if request.method == 'GET':
        properties = PlayerProperties.query.filter_by(user_id=user.id).first()
        return jsonify(
            experience=properties.experience,
            if_chef_orders=properties.if_chef_orders,
            if_waiter_orders=properties.if_waiter_orders,
            for_chef_orders=properties.for_chef_orders,
            for_waiter_orders=properties.for_waiter_orders,
            put_chef_orders=properties.put_chef_orders,
            put_waiter_orders=properties.put_waiter_orders
        )
    
    if request.method == 'PUT':
        data = request.get_json()
        properties = PlayerProperties.query.filter_by(user_id=user.id).first()
        properties.experience = data.get('experience', properties.experience)
        properties.if_chef_orders = data.get('if_chef_orders', properties.if_chef_orders)
        properties.if_waiter_orders = data.get('if_waiter_orders', properties.if_waiter_orders)
        properties.for_chef_orders = data.get('for_chef_orders', properties.for_chef_orders)
        properties.for_waiter_orders = data.get('for_waiter_orders', properties.for_waiter_orders)
        properties.put_chef_orders = data.get('put_chef_orders', properties.put_chef_orders)
        properties.put_waiter_orders = data.get('put_waiter_orders', properties.put_waiter_orders)
        db.session.commit()
        return jsonify({"message": "Properties updated successfully"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
