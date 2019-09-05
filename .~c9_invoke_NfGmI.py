import os
from flask import Flask, render_template, redirect, request, url_for, current_app
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from form import AddForm
from werkzeug import secure_filename
from constants import country_mapping, cuisine_mapping


app = Flask(__name__)

app.config['SECRET_KEY'] = 'any secret key'
app.config['IMAGES_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/images/')
app.config["MONGO_DBNAME"] = 'diy_cookery'
app.config["MONGO_URI"] = "mongodb+srv://root:r00tUser@myfirstcluster-q10cc.mongodb.net/diy_cookery?retryWrites=true&w=majority"


#csrf = CSRFProtect(app)
mongo = PyMongo(app)


@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    recipes=mongo.db.recipes.find()
    return render_template("recipes.html",
    recipes=recipes)
    

def populate_form(form_data, image_name=None):
    form_data['country'] = country_mapping[form_data.get('country')]
    form_data['cuisine'] = cuisine_mapping[form_data.get('cuisine')]
    form_data['ingredients'] =  form_data.get('ingredients').split(';')
    form_data['methods'] =  form_data.get('methods').split(';')
    if image_name is not None:
        form_data['image'] = image_name
    
    return form_data
    
@app.route('/add_recipe', methods=["GET", "POST"])
def add_recipe():

        form = AddForm()
        if request.method == 'POST' :
            if form.validate_on_submit():
                # Get the image from the submitted form
                image = request.files.get('file')
                
                # Get the submitted form and perform the required
                # manipulation
                form_data = request.form.to_dict()
                form_data = populate_form(form_data, image_name=image.filename) if image else populate_form(form_data)
                
                # Saves the image to the file system
                if image:
                    image.save(os.path.join(app.config.get('IMAGES_FOLDER'), image.filename))
                
                recipes = mongo.db.recipes
                recipes.insert_one(form_data)
                return redirect(url_for('get_recipes'))

        # Implicit GET request
        return render_template("addrecipe.html", form = form, cuisines=mongo.db.cuisines.find(),
        countries=mongo.db.countries.find())
        
        
    
@app.route('/view_recipe/<recipe_id>')
def view_recipe(recipe_id):
    all_recipes = mongo.db.recipes.find({"_id": ObjectId(recipe_id)})
    return render_template("viewrecipe.html", recipes = all_recipes)
    



# @app.route('/insert_recipe', methods=["POST"])
# def insert_recipe():
    
#     form = AddForm()
#     if form.validate_on_submit() == False:
#         return redirect(url_for('add_recipe'))
#         #return render_template("addrecipe.html", form = form, cuisines = mongo.db.cuisines.find(), countries=mongo.db.countries.find())
        
#     else:
#         return render_template("addrecipe.html")
#         return redirect(url_for('get_recipes'))
  

@app.route('/edit_recipe/<recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    form = AddForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        # Get the image from the submitted form
        image = request.files.get('file')
        
        # Get the submitted form and perform the required
        # manipulation
        form_data = request.form.to_dict()
        form_data = populate_form(form_data, image_name=image.filename) if image else populate_form(form_data)
        
        # Saves the image to the file system
        if image:
            image.save(os.path.join(app.config.get('IMAGES_FOLDER'), image.filename))

        recipes = mongo.db.recipes
        recipes.update({'_id': ObjectId(recipe_id)}, form_data)
        return redirect(url_for('get_recipes'))
        
    # Implicit GET request
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    form.recipe.data = the_recipe.get('recipe')
    form.allergens.data = the_recipe.get('allergens')
    
    form.ingredients.data = '; '.join(the_recipe.get('ingredients'))
    form.methods.data = '; '.join(the_recipe.get('methods'))

    form.cuisine.data = next(k for k,v in cuisine_mapping.items() if v == the_recipe.get('cuisine'))
    form.country.data = next(k for k,v in country_mapping.items() if v == the_recipe.get('country'))
    
    all_cuisines = mongo.db.cuisines.find()
    all_countries = mongo.db.countries.find()
    
    return render_template('editrecipe.html', recipe = the_recipe, form = form, cuisines=all_cuisines, countries=all_countries)
    
    
# @app.route('/update_recipe/<recipe_id>', methods=["POST"])
# def update_recipe(recipe_id):
#     recipes = mongo.db.recipes
#     recipes.update( {'_id': ObjectId(recipe_id)},
#     {
#         'cuisine_name': request.form.get('cuisine_name'),
#         'recipe_name': request.form.get('recipe_name'),
#         'recipe_allergens': request.form.get('recipe_allergens'),
#         'recipe_ingredients': request.form.get('recipe_ingredients'),
#         'recipe_methods': request.form.get('recipe_methods')
        
#     })
#     return redirect(url_for('get_recipes'))
    

@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))
   
   
   
   
    # Cuisines 
    
@app.route('/get_cuisines')
def get_cuisines():
    cuisines=mongo.db.cuisines.find()
    print (cuisines)
    return render_template('cuisines.html', recipes=mongo.db.cuisines.find())
    
    
@app.route('/view_cuisine/<recipe_id>')
def view_cuisine(recipe_id):
    all_recipes = mongo.db.recipes.find({"_id": ObjectId(recipe_id)})
    return render_template("viewcuisine.html", recipes = all_recipes)
    
    
@app.route('/edit_cuisine/<cuisine_id>')
def edit_cuisine(cuisine_id):
    return render_template('editcuisine.html', 
    cuisine=mongo.db.cuisines.find_one({'_id': ObjectId(cuisine_id)}))
    

    
@app.route('/update_cuisine/<cuisine_id>', methods=['POST'])
def update_cuisine(cuisine_id):
    mongo.db.cuisines.update(
        {'_id': ObjectId(cuisine_id)},
        {'cuisine_name': request.form.get['cuisine_name']})
    return redirect(url_for('get_cuisines'))
    
    
    

# wont work
@app.route('/delete_cuisine/<cuisine_id>')
def delete_cuisine(cuisine_id):
    mongo.db.cuisines.remove({'_id': ObjectId(cuisine_id)})
    return redirect(url_for('get_cuisines'))
    
    
    

@app.route('/insert_cuisine', methods=['POST'])
def insert_cuisine():
    cuisines = mongo.db.cuisines
    cuisines.insert_one(request.form.to_dict())
    return redirect(url_for('get_cuisines'))
    
    
    
    # wont work
@app.route('/add_cuisine', methods=["GET", "POST"])
def add_cuisine():

        form = AddForm()
        if request.method == 'POST' :
            if form.validate_on_submit():
                cuisines = mongo.db.cuisines
                cuisines.insert_one('cuisines')
                return redirect(url_for('get_cuisines'))

        # Implicit GET request
        return render_template("addcuisine.html", form = form, cuisines=mongo.db.cuisines.find())


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)