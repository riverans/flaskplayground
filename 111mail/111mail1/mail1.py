'''
'value' column has a select list in the edit form.

ref. 
https://gist.github.com/mrjoes/3714266#file-templates_color_list-html

'''
from flask import Flask
from flask.ext import admin, wtf
from flask.ext.admin.contrib.sqla import filters
from flask.ext.admin.model import template
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.widgets import Select2Widget
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property, relationship
from sqlalchemy.orm import relationship
from wtforms import SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
import flask_admin as admin

# Create application
app = Flask(__name__)

# Create dummy secret key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# Create models
class Color(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    value = db.Column(db.String(8))

# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'

# Color admin with custom template
class ColorAdmin(ModelView):
    # Force specific template
    list_template = 'color_list.html'
    create_template = 'color_form.html'
    edit_template = 'color_form.html'

    # Customize list view to call 'color' macro for value column
    list_formatters = dict(value=template.macro('color'))

    # Use select field for value column
    form_overrides = dict(value=SelectField)

    form_args = dict(value=dict(
        choices=[
            ('#000000', 'Black'),
            ('#ffffff', 'White'),
            ('#ff0000', 'Red'),
            ('#00ff00', 'Green'),
            ('#0000ff', 'Blue'),
        ]))

if __name__ == '__main__':
    # Create admin
    admin = admin.Admin(app, 'Simple Models')

    # Add views
    admin.add_view(ColorAdmin(Color, db.session))

    # Create DB
    db.create_all()

    # Start app
    app.debug = True
    app.run('0.0.0.0', 5000)
    