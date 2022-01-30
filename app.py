import os
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for, logging)
from wtforms import (
    Form, StringField, TextAreaField, PasswordField, validators)
from passlib.hash import sha256_crypt
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
# from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# ---------------- Forms ----------------

class SignupForm(Form):
    name = StringField('Name', [validators.Length(min=2, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=20)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm_password = PasswordField('Confirm Password')

# ---------------- End Forms ----------------


# ---------------- Routes ----------------
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/articles")
def articles():
    return render_template('articles.html')


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        signup_user = {
            'name': request.form.get('name').lower(),
            'email': request.form.get('email').lower(),
            'username': request.form.get('username').lower(),
            'password': sha256_crypt.hash(request.form.get('password'))
        }
        # insert_one requires an dictionary to store info in mongoDB
        mongo.db.users.insert_one(signup_user)

        flash('You have Signed Up successfully! Please proceed to Login', 'success')
        redirect(url_for('articles'))

    return render_template('signup.html', form=form)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
    port = int(os.environ.get("PORT")),
    debug = True)
