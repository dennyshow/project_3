from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SubmitField, FileField, SelectField
from wtforms import validators, ValidationError
from wtforms.validators import DataRequired


class AddForm(FlaskForm):
    cuisine = SelectField("Cuisine Name",
                                    choices = [('', 'Select a Cuisine'), 
                                    ('eu', 'European Cuisine'),
                                    ('af', 'African Cuisine'), 
                                    ('ie', 'Irish Cuisine'), 
                                    ('ch', 'Chinese Cuisine')])
    file = FileField('Add Cuisine Image')                    
    recipe = TextField("Recipe Name", validators=[DataRequired()])
    allergens = TextField("Recipe Allergens", validators=[DataRequired()])
    ingredients = TextAreaField("Recipe Ingredients", validators=[DataRequired()])
    methods = TextAreaField("Recipe Methods", validators=[DataRequired()])
    
    country = SelectField("Country of Origin", choices = [
                                                ('', 'Select a Country'),
                                                ('it', 'Italy'),
                                                ('ng', 'Nigeria'), 
                                                ('ie', 'Ireland'), 
                                                ('ch', 'China')])
    
    def validate_cuisine(self, cuisine):
        if cuisine.data == "":
            raise ValidationError("Kindly select a cuisine")
            
    def validate_country(self, country):
        if country.data == "":
            raise ValidationError("Kindly select a country")
            

class FilterForm(FlaskForm):
    cuisine = SelectField("Cuisine Name",
                                    choices = [('', 'Select a Cuisine'), 
                                    ('eu', 'European Cuisine'),
                                    ('af', 'African Cuisine'), 
                                    ('ie', 'Irish Cuisine'), 
                                    ('ch', 'Chinese Cuisine')])
    country = SelectField("Country of Origin", choices = [
                                                ('', 'Select a Country'),
                                                ('it', 'Italy'),
                                                ('ng', 'Nigeria'), 
                                                ('ie', 'Ireland'), 
                                                ('ch', 'China')])                                    