from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.model_user import User
from flask_app.models.model_recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



#go to NEW RECIPE page
@app.route('/recipes/new')
def new_recipe_page():
    if 'user_id' not in session:
        return redirect ('/')
    data = {
        'id': session['user_id']
    }
    user=User.get_by_id(data)
    return render_template('new_recipe.html',user=user )

#create a new recipe
@app.route('/create/recipe',methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.is_valid(request.form):
        return redirect('/new/recipe')
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "under30": request.form["under30"],
        "date_made": request.form["date_made"],
        "user_id": session["user_id"]
    }
    Recipe.save(data)
    return redirect('/dashboard')

#go to EDIT RECIPE page
@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect ('/')
    data = {
        'id': id
    }
    user_data={
        'id': session['user_id']
    }
    user=User.get_by_id(user_data)
    recipe = Recipe.get_one(data)
    return render_template('edit_recipe.html', recipe=recipe, user=user)

#edit the recipe
@app.route('/recipes/update', methods=['POST'])
def update():
    if 'user_id' not in session:
        return redirect ('/')
    if not Recipe.is_valid(request.form):
        return redirect ('/dashboard')
    data = {
        "id": request.form["id"],
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "under30": request.form["under30"],
        "date_made": request.form["date_made"],
        "user_id": session["user_id"]
    }
    print(data)
    Recipe.update_one(data)

    return redirect ('/dashboard')

#go to SHOW RECIPE page
@app.route('/recipes/<int:id>')
def show_recipe(id):
    if 'user_id' not in session:
        return redirect ('/')
    data = {
        'id': id
    }
    user_data={
        'id': session['user_id']
    }
    user=User.get_by_id(user_data)
    recipe = Recipe.get_one(data)
    return render_template('show_recipe.html', recipe=recipe, user=user)



#delete recipe
@app.route('/recipes/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect ('/')
    data = {
        'id':id
        }
    Recipe.delete(data)
    return redirect ('/dashboard')