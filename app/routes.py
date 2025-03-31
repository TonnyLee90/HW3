from app import myapp_obj
from flask import render_template
from flask import redirect, url_for, flash
from app.forms import RecipeForm, RegisterForm, LoginForm
from app.models import User, Recipe
from app import db, login_manager
from flask_login import login_user, login_required, current_user, logout_user

# To register
@myapp_obj.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        # add the user to the db
        db.session.add(user)
        db.session.commit
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# To log in
@myapp_obj.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # to check if the username entered in the form == the username in the db
        user = User.query.filter_by(username=form.username.data).first()
        if user: # if find the user in db and the password is correct
            login_user(user) # to login
            return redirect(url_for('home'))
    return render_template('login.html', form=form)

# To load the user the user, when user login in
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# To login out the user
@myapp_obj.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('/')) # after loggin out, redirect to the home page

# Home page: Shows all the recipes (unordered list)
# All visitors can visit this page
@myapp_obj.route('/')
@myapp_obj.route('/recipes')
def home():
    recipes = Recipe.query.all() # search all recipes from the db
    return render_template('home.html', recipes=recipes)

# This page is used to add a new recipe
@myapp_obj.route('/recipe/new', methods=['GET', 'POST'])
@login_required
def new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(title=form.title.data, description=form.description.data,
                        ingredients=form.ingredients.data, instructions=form.instructions.data,
                        user=current_user)
        # Save the data entered in the form to the db
        db.session.add(recipe)
        db.session.commit()

        flash('Recipe added successfully!')

        return redirect(url_for('home'))
    return render_template('new_recipe.html', form=form)

# this page is used to show a detailed recipe
@myapp_obj.route('/recipe/<int:recipe_id>')
@login_required
def recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id) # Search a recipe by id, if it's not found, return error 404
    return render_template('recipe.html', recipe=recipe)

# this page is used to delete a recipe
@myapp_obj.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id) # Search a recipe by id, if it's not found, return error 404
    if recipe.author != current_user: # Check if the recipe's user != current_user
        flash('You do not have permission to delete')
        return redirect(url_for('home'))
    
    # delete the post
    db.session.delete(recipe)
    db.session.commit()

    flash('Recipe deleted!')

    return redirect(url_for('home'))
