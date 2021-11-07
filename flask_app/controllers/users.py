from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) #create object called bcrypt 


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register/user', methods = ['POST'])
def register():
    if not User.validate(request.form):
        return redirect('/')
    #create hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    user_id = User.save(data) #save new user id
    if not user_id:
        flash("Something went wrong!")
        return redirect('/')
    session['user_id'] = user_id #store user id in session (logged in)
    return redirect("/dashboard")

@app.route('/login', methods=['POST'])
def login():
    data = {
        'email':request.form['email']
    }
    user = User.get_from_email(data)

    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("wrong password", "login")
        return redirect('/')
    session['user_id']=user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if "user_id" not in session: #check if user is logged in to see dashboard
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    user = User.get_one_user(data)
    recipes = Recipe.get_all_recipes()
    return render_template('dashboard.html', the_user = user, all_recipes = recipes)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
