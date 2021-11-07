from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe



@app.route("/recipe/new")
def new_recipe():
    if "user_id" not in session: #check if user is logged in to see dashboard
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    user = User.get_one_user(data)
    return render_template("recipe_new.html", the_user = user)

@app.route('/recipe/create', methods=["POST"])
def create_recipe():
    if "user_id" not in session: #check if user is logged in to see dashboard
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipe/new')
    data = {
        "name":request.form["name"],
        "description": request.form["description"],
        "instruction":request.form["instruction"],
        "under30":int(request.form["under30"]),
        "date_made":request.form["date_made"],
        "user_id": request.form["user_id"]
    }
    print(f"created data: {data}")
    Recipe.save(data)
    return redirect('/dashboard')

@app.route('/recipe/edit/<int:id>')
def edit_recipe(id):
    if "user_id" not in session: #check if user is logged in to see dashboard
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        'id': session['user_id']
    }
    user = User.get_one_user(user_data)
    return render_template("recipe_edit.html", recipe = Recipe.get_one_recipe(data), the_user=user)

@app.route('/recipe/update', methods=['POST'])
def update_recipe():
    if "user_id" not in session: #check if user is logged in to see dashboard
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect(f"/recipe/edit/{request.form['recipe_id']}")
    data ={
        "id":request.form['recipe_id'],
        "name":request.form["name"],
        "description": request.form["description"],
        "instruction":request.form["instruction"],
        "under30":int(request.form["under30"]),
        "date_made": request.form["date_made"],
        "user_id": request.form["user_id"]
    }
    print(f"printing update data {data}")
    Recipe.update(data)
    return redirect('/dashboard')

@app.route('/recipe/show/<int:id>')
def show_recipe(id):
    if "user_id" not in session: #check if user is logged in to see dashboard
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data ={
        "id":session['user_id']
    }
    return render_template("recipes.html", recipe = Recipe.get_one_recipe(data), the_user = User.get_one_user(user_data))

@app.route('/recipe/destroy/<int:id>')
def destroy(id):
    if "user_id" not in session: #check if user is logged in to see dashboard
        return redirect('/logout')
    data={
        'id':id
    }
    Recipe.destroy(data)
    return redirect('/dashboard')