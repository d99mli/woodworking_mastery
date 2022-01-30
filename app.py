import os
from functools import wraps
from flask import (
    Flask, flash, render_template, redirect, request,
    session, url_for, logging)
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


# -------------------------------- Forms --------------------------------
# Register / Signin
class SignupForm(Form):
    name = StringField('Name', [validators.Length(min=2, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=20)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo(
            'confirm_password', message='Passwords do not match')
    ])
    confirm_password = PasswordField('Confirm Password')


# Article add/edit/update
class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=2, max=200)])
    body = TextAreaField('Body', [validators.Length(min=20)])

# -------------------------------- End Forms ------------------------------

# -------------------------------- function decorator ---------------------


# Check if user logged in (function decorator)
def is_signed_in(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'user_signed_in' in session:
            return func(*args, **kwargs)
        else:
            flash('Unauthorized, please sign in!', 'danger')
            return redirect(url_for('signin'))
    return wrap
# -------------------------------- End function --------------------------


# -------------------------------- Routes --------------------------------
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


# --- Articles ---
@app.route("/articles")
def articles():
    return render_template('articles.html')


# --- Add Article ---
@app.route('/add_article', methods=['GET', 'POST'])
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        one_article = {
            'title': request.form.get('title'),
            'body': request.form.get('body'),
            'category': request.form.get('category')
        }
        # insert_one requires an dictionary to store info in mongoDB
        mongo.db.articles.insert_one(one_article)

        flash('Article successfully posted!', 'success')
        return redirect(url_for('articles'))
    return render_template('add_article.html', form=form)


# --- User Account (profile) Page ---
@app.route('/account')
@is_signed_in
def account():
    return render_template('account.html')


# --- Sign up ---
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

        flash('You have Signed Up successfully!', 'success')
        return redirect(url_for('signin'))

    return render_template('signup.html', form=form)


# --- Sign in ---
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignupForm(request.form)
    if request.method == 'POST':
        # Check if user exists in db
        user_signin = mongo.db.users.find_one(
            {'email': request.form.get('email').lower()}
        )

        if user_signin:
            # Ensure hashed passwords matches user input
            if sha256_crypt.verify(
                    request.form.get('password'), user_signin['password']):

                # Create session cookie for signed in user
                session['user_signed_in'] = True
                session['email'] = request.form.get('email').lower()
                flash('Welcome, {}'.format(
                    request.form.get('email')), 'success')
                return redirect(url_for('articles'))

            else:
                # Invalid Email/password match
                flash('Incorrect Email and/or Password', 'danger')
                return redirect(url_for('signin'))

        else:
            # User doesn't exist
            flash('Incorrect Email and/or Password', 'danger')
            return redirect(url_for('signin'))

    return render_template('signin.html', form=form)


# --- Sign Out ---
@app.route('/signout')
@is_signed_in
def signout():
    session.clear()
    flash('You have successfully signed out!', 'success')
    return redirect(url_for('signin'))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
