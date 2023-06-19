from flask_app import app
from flask import render_template, session, redirect, request, flash
from flask_app.models.recipe import Recipe
from datetime import datetime

#! Create
@app.route("/recipes/new")
def new_recipe_form():
        if 'user_id' not in session:
                return redirect("/")
        return render_template("new_recipe.html")

@app.route("/recipes/create", methods = ["POST", "GET"])
def create_recipe():
        if 'user_id' not in session:
                return redirect("/")
        if request.method == "POST":
                if not Recipe.validate_recipe(request.form):
                        return redirect("/recipes/new")
        data = {
                'name': request.form['name'],
                'description': request.form['description'],
                'instructions': request.form['instructions'],
                'datemade': request.form['datemade'],
                'time': request.form['time'],
                'user_id': session['user_id']
        }
        print(data)
        Recipe.create_recipe(data)
        return redirect("/dashboard")

#! Read
@app.route("/recipes/view/<int:recipe_id>") # Change to /recipes/views/<int:id> later
def view_recipe(recipe_id):
        if 'user_id' not in session:
                return redirect("/")
        recipe = Recipe.get_recipe_by_id({'id': recipe_id})
        formatted_date = recipe.datemade.strftime('%B %dth, %Y') #! HERE
        return render_template("view_recipe.html", recipe = recipe, formatted_date = formatted_date)

#! Update
@app.route("/recipes/edit/<int:recipe_id>") # Add /<int:id> to this later
def edit_recipe_page(recipe_id):
        if 'user_id' not in session:
                return redirect("/")
        user_id = session['user_id']
        recipe = Recipe.get_recipe_by_id({'id': recipe_id})
        if not recipe or recipe.chef.id != user_id:     # Ensures a user cannot type an edit address into their browser to see someone else's edit page.
                return redirect("/dashboard")
        return render_template("edit_recipe.html", recipe = recipe)

@app.route("/recipes/update", methods=["POST"])
def update_recipe():
        if 'user_id' not in session:
                return redirect("/")
        if request.method == "POST":
                if not Recipe.validate_recipe(request.form):
                        recipe_id = request.form['id']
                        return redirect(f"/recipes/edit/{recipe_id}")
        # Validation here later
        Recipe.edit_one_recipe(request.form)
        return redirect("/dashboard")

#! Delete
@app.route("/recipes/delete/<int:recipe_id>")
def delete_recipe(recipe_id):
        if 'user_id' not in session:
                return redirect("/")
        user_id = session['user_id']
        recipe = Recipe.get_recipe_by_id({'id': recipe_id})
        if not recipe or recipe.chef.id != user_id:     # Ensures a user cannot delete someone else's recipe.
                return "You are not authorized to delete this recipe. Press the back button in your browser and stop being weird."
        Recipe.delete_recipe(recipe_id)
        return redirect("/dashboard")