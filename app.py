                # Flask packages imports

import os
from flask import Flask, render_template, redirect, request, url_for, current_app, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from form import AddForm, FilterForm
from werkzeug import secure_filename
from constants import country_mapping, cuisine_mapping


app = Flask(__name__)

            # config for WTForms
            # config for image storage 
            # config for MONGO DB

app.config['SECRET_KEY'] = 'any secret key'
app.config['IMAGES_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/images/')
app.config["MONGO_DBNAME"] = 'diy_cookery'
app.config["MONGO_URI"] = "mongodb+srv://root:r00tUser@myfirstcluster-q10cc.mongodb.net/diy_cookery?retryWrites=true&w=majority"

mongo = PyMongo(app)


                                    ####### RECIPES #####



@app.route('/', methods=['GET', 'POST'])
def get_recipes():
    
        # creating and passing url params
        # creating and passing request.args
    
    cuisine, country = None, None
    
    if request.args.get('cuisine'):
        cuisine = cuisine_mapping.get(request.args.get('cuisine'))
    if request.args.get('country'):
        country = country_mapping.get(request.args.get('country'))
        
    if cuisine or country:
        recipes = mongo.db.recipes.find({
                                    '$or': [dict(country=country), dict(cuisine=cuisine)]
        })
         
        # Passing result of args into filters
        # And passing each matching _id into filters

        result = []
        for recipe in recipes:
            recipe_ = dict(cuisine=recipe['cuisine'], recipe=recipe['recipe'], allergens=recipe['allergens'], ingredients=recipe['ingredients'],
            methods=recipe['methods'], country=recipe['country'], image=recipe.get('image'), _id=recipe['_id'])
            result.append(recipe_)
    else:
        result=mongo.db.recipes.find()

       # using POST method to determine filter-form on request
        
    form = FilterForm()
    if request.method == "POST":
        return redirect(url_for('get_recipes', country=form.country.data, cuisine=form.cuisine.data))
 
    return render_template("recipes.html",
    recipes=result, form=form)
    


                                ####### Pre-population of Form Fields #####

def populate_form(form_data, image_name=None):
    form_data['country'] = country_mapping[form_data.get('country')]
    form_data['cuisine'] = cuisine_mapping[form_data.get('cuisine')]
    form_data['ingredients'] =  form_data.get('ingredients').split(';')
    form_data['methods'] =  form_data.get('methods').split(';')
    if image_name is not None:
        form_data['image'] = image_name
    
    return form_data
    

                            ####### ADDING RECIPE #####


    
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
        


        
                        ####### VIEW RECIPE #####

        
        
    
@app.route('/view_recipe/<recipe_id>', methods=["GET", "POST"])
def view_recipe(recipe_id):
    all_recipes = mongo.db.recipes.find({"_id": ObjectId(recipe_id)})
    return render_template("viewrecipe.html", recipes = all_recipes)



                    ####### EDIT RECIPE #####


  

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
    

                ####### DELETE RECIPE #####

    

@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))
   
   
   
                        ####### CUISINES #####
    


    

@app.route('/')
@app.route('/get_cuisines')
def get_cuisines():
    cuisines=mongo.db.cuisines.find()
    return render_template("cuisines.html",
    cuisines=cuisines)


                     ####### ADDING CUISINE #####

 
    
@app.route('/add_cuisine', methods=["GET", "POST"])
def add_cuisine():

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
                
                cuisines = mongo.db.cuisines
                cuisines.insert_one(form_data)
                return redirect(url_for('get_cuisines'))

        # Implicit GET request
        return render_template("addcuisine.html", form = form, cuisines=mongo.db.cuisines.find(),
        countries=mongo.db.countries.find())
    


                     ####### VIEW CUISINE #####

    
@app.route('/view_cuisine/<cuisine_id>')
def view_cuisine(cuisine_id):
    all_cuisines = mongo.db.cuisines.find({"_id": ObjectId(cuisine_id)})
    return render_template("viewcuisine.html", cuisines = all_cuisines)
    
 
 
                    ####### EDIT CUISINE #####


  
@app.route('/edit_cuisine/<cuisine_id>', methods=['GET', 'POST'])
def edit_cuisine(cuisine_id):
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

        cuisines = mongo.db.cuisines
        cuisines.update({'_id': ObjectId(cuisine_id)}, form_data)
        return redirect(url_for('get_cuisines'))
        
    # Implicit GET request
    the_cuisine = mongo.db.cuisines.find_one({"_id": ObjectId(cuisine_id)})
    form.cuisine.data = the_cuisine.get('recipe')
    form.allergens.data = the_cuisine.get('allergens')
    
    form.ingredients.data = '; '.join(the_cuisine.get('ingredients'))
    form.methods.data = '; '.join(the_cuisine.get('methods'))

    form.cuisine.data = next(k for k,v in cuisine_mapping.items() if v == the_cuisine.get('cuisine'))
    form.country.data = next(k for k,v in country_mapping.items() if v == the_cuisine.get('country'))
    
    all_cuisines = mongo.db.cuisines.find()
    all_countries = mongo.db.countries.find()
    
    return render_template('editcuisine.html', cuisine = the_cuisine, form = form, cuisines=all_cuisines, countries=all_countries)
    


                    ####### DELETE CUISINE #####


@app.route('/delete_cuisine/<cuisine_id>')
def delete_cuisine(cuisine_id):
    mongo.db.cuisines.remove({'_id': ObjectId(cuisine_id)})
    return redirect(url_for('get_cuisines'))
    
            
        
    
    

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)