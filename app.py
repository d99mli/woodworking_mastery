import os
from functools import wraps
from datetime import datetime
from flask import (
    Flask, flash, render_template, redirect, request,
    session, url_for)
from wtforms import (
    Form, StringField, TextAreaField, PasswordField)
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
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
# Register / Sign Up
class SignupForm(Form):
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=2, max=50),
    ])
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=20),
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Regexp(
            '^[a-zA-Z0-9.!#$%&*+/=?_~-]+@[a-zA-Z0-9-]+(?:\\.[a-zA-Z0-9-]+)*$',
            message="Must be a valid e-mail")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo(
            'confirm_password', message='Passwords do not match')
    ])
    confirm_password = PasswordField('Confirm Password')


# Sign In
class SigninForm(Form):
    email = StringField('Email', validators=[
        DataRequired(),
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
    ])


# Article add/edit/update
class ArticleForm(Form):
    title = StringField('Title', validators=[
        DataRequired(),
        Length(min=2, max=50),
    ])
    content = TextAreaField('Content', validators=[
        DataRequired(),
    ])

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


@app.route("/about")
def about():
    return render_template('about.html')


# --- Articles ---
@app.route("/articles")
def articles():
    all_articles = mongo.db.articles.find()
    return render_template('articles.html', articles=all_articles)


# --- One article ---
@app.route("/article/<article_id>")
def one_article(article_id):
    article_id = mongo.db.articles.find_one(
        {'_id': ObjectId(article_id)}
    )
    return render_template('one_article.html', article_id=article_id)


# --- Add Article ---
@app.route('/add_article', methods=['GET', 'POST'])
@is_signed_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():

        new_article = {
            'title': request.form.get('title'),
            'content': request.form.get('content'),
            'author': session["user_signed_in"],
            "create_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # insert_one requires an dictionary to store info in mongoDB
        mongo.db.articles.insert_one(new_article)

        flash('Article successfully posted!', 'success')
        return redirect(url_for('articles'))

    return render_template('add_article.html', form=form)


# --- Edit Article ---
@app.route("/edit_article/<article_id>", methods=['GET', 'POST'])
@is_signed_in
def edit_article(article_id):
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():

        one_article = {
            'title': request.form.get('title'),
            'content': request.form.get('content'),
            'author': session["user_signed_in"],
            "create_date": datetime.now().strftime('%Y-%m-%d %H:%M')
        }

        mongo.db.articles.update({"_id": ObjectId(article_id)}, one_article)
        flash('Article Successfully Updated!', 'success')
        return redirect(url_for('account'))

    article = mongo.db.articles.find_one({"_id": ObjectId(article_id)})
    form.title.data = article['title']
    form.content.data = article['content']

    return render_template('edit_article.html', article=article, form=form)


# --- Delete article ---
@app.route('/delete_article/<article_id>')
@is_signed_in
def delete_article(article_id):
    mongo.db.articles.remove({"_id": ObjectId(article_id)})
    flash('Article sucessfully removed!', 'success')
    return redirect(url_for('account'))


# --- User Account (profile) Page ---
@app.route('/account')
@is_signed_in
def account():
    all_articles = mongo.db.articles.find()
    return render_template('account.html', articles=all_articles)


# --- Sign up ---
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        # check if user already exists in db
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})

        if existing_user:
            flash('Email already listed. Please proceed to Sign In', 'warning')
            return redirect(url_for('signin'))

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
    form = SigninForm(request.form)
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
                session['user_signed_in'] = request.form.get("email")
                flash("Welcome, {}".format(
                    request.form.get("email")), 'success')
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
            debug=False)
