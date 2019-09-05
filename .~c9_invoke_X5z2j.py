from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, FileField, SelectField
from wtforms import validators, ValidationError
from wtforms.validators import DataRequired



class AddForm(Form):
    cuisine = SelectField("Cuisine Name", choices = [('European Cuisine'),('African Cuisine'), ('Irish Cuisine'), ('Chinese Cuisine')])
    #recipe = TextField("Recipe Name", [validators.Required("Please enter your recipe.")])
    recipe = TextField("Recipe Name", validators=[DataRequired("Please enter you)])
    #allergens = TextField("Recipe Allergens", [validators.Required("Please enter allergen.")])
    allergens = TextField("Recipe Allergens", validators=[DataRequired("Please enter your allergen")])
    ingredients = TextAreaField("Recipe Ingredients")
    methods = TextAreaField("Recipe Methods")
    
    country = SelectField("Country of Origin", validators=[DataRequired("Please enter your country.")], choices = [('Italy'),('Nigeria'), ('Ireland'), ('China')])
    submit = SubmitField("Add Recipe")





















