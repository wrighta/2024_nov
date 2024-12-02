import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

# from flask_migrate import Migrate
# from flask_script import Manager
from models import db, Category, Recipe 


# Path for saving uploaded images
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# Create the Flask application instance
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://receipe_db_x4z3_user:9BTJONCJXozP65Wt0sEMyb7tkCOcMEmR@dpg-csv1ob52ng1s73dqv3i0-a.frankfurt-postgres.render.com/receipe_db_x4z3'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flask_user:yourpassword@localhost/recipes_db'



#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flask_user:yourpassword@localhost/recipes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialise SQLAlchemy
db.init_app(app)


# Set the static folder
app.config['STATIC_FOLDER'] = 'static'

# Define routes
@app.route('/')
def home():
    categories = Category.query.all()
    return render_template('index.html', categories=categories)

@app.route('/recipes')
def recipes():
    all_recipes = Recipe.query.all()  # Fetch all recipes
    return render_template('recipes.html', recipes=all_recipes)

@app.route('/recipe/<int:id>')
def recipe_detail(id):
    recipe = Recipe.query.get_or_404(id)
    return render_template('recipe.html', recipe=recipe)

@app.route('/recipes/<int:category_id>')
def category_recipes(category_id):
    category = Category.query.get_or_404(category_id)
    recipes = Recipe.query.filter_by(category_id=category_id).all()
    return render_template('recipes.html', category=category, recipes=recipes)


@app.route('/about')
def about():
    return render_template('about.html')


# Helper function to validate allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# create_recipe can be a GET or POST request
@app.route('/create_recipe', methods=['GET', 'POST'])
def create_recipe():
    # POST - saves the recipe to the database
    if request.method == 'POST':
        # Get form data
        title = request.form['title']
        description = request.form['description']
        ingredients = request.form['ingredients']
        category_id = request.form['category_id']

        # Handle file upload
        file = request.files['image']
        if file and allowed_file(file.filename):
            # Secure filename and save to upload folder
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            flash('Invalid file type. Only PNG, JPG, JPEG, and GIF are allowed.', 'danger')
            return redirect(request.url)

        # Create a new Recipe object
        new_recipe = Recipe(
            title=title,
            description=description,
            ingredients=ingredients,
            category_id=category_id,
            image=filename  # Save the image filename to the database
        )

        # Save to the database
        try:
            db.session.add(new_recipe)
            db.session.commit()
            flash('Recipe created successfully!', 'success')
            return redirect(url_for('recipes'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {e}', 'danger')
            return redirect(request.url)

    # GET - loads the create_recipe html page
    # Fetch categories for the dropdown 
    categories = Category.query.all()
    return render_template('create_recipe.html', categories=categories)

@app.route('/edit_recipe/<int:id>', methods=['GET', 'POST'])
def edit_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    # POST so I am updating the recipe in the database
    if request.method == 'POST':
        # Update recipe details from form
        recipe.title = request.form['title']
        recipe.description = request.form['description']
        recipe.ingredients = request.form['ingredients']
        recipe.category_id = request.form['category_id']
        # Handle image upload if needed
        if 'image' in request.files and request.files['image']:
            image = request.files['image']
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.static_folder, 'images', filename))
            recipe.image = filename
        db.session.commit()
        flash('Recipe updated successfully!', 'success')
        return redirect(url_for('recipes'))
    # GET - so I am loading the edit recipe page
    categories = Category.query.all()
    return render_template('edit_recipe.html', recipe=recipe, categories=categories)


@app.route('/delete_recipe/<int:id>', methods=['POST'])
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    try:
        db.session.delete(recipe)
        db.session.commit()
        flash('Recipe deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting recipe: {e}', 'danger')

    return redirect(url_for('recipes'))



@app.route('/contact')
def contact():
    return render_template('contact.html')

# Create a Flask-Script manager instance

# Add commands to the manager for database management

# Run the application if executed directly
if __name__ == '__main__':
    app.run(debug=True)
