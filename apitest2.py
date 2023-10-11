from flask import Flask, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
from flask_login import current_user


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "abc"
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

db.init_app(app)

with app.app_context():
    db.create_all()
    

@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)


@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if not username or not password:
            return jsonify({"message": "Username and password are required"}), 400

        user = Users(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        
        return jsonify({"message": "User registered successfully"}), 201
    

@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = Users.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"message": "Invalid username or password"}), 401

# @app.route("/logout")
# def logout():
#     logout_user()
#     return jsonify({"message": "Logged out successfully"}), 200

@app.route("/logout",methods=['GET'])
def logout():
    if current_user.is_authenticated:
        
        db.session.delete(current_user)
        db.session.commit()
        logout_user()
        return jsonify({"message": "Logged out successfully and user data deleted"}), 200
    else:
        return jsonify({"message": "User is not logged in"}), 401


@app.route("/")
def home():
    return jsonify({"message": "Welcome to the API"}), 200


if __name__ == "__main__":
    app.run(debug=True)
    
    
    
    
    
    
    
    
    
    
    
