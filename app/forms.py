from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, validators

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[validators.InputRequired()])
    password = PasswordField('Password', validators=[validators.InputRequired()])
    submit =  SubmitField("Register!")

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[validators.InputRequired()])
    password = PasswordField('Password', validators=[validators.InputRequired()])
    submit =  SubmitField("Login")

class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[validators.InputRequired()])
    description = TextAreaField('Description', validators=[validators.InputRequired()])
    ingredients = TextAreaField('Ingredients', validators=[validators.InputRequired()])
    instructions = TextAreaField('Instructions', validators=[validators.InputRequired()])
    submit = SubmitField('Submit!')