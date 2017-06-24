from flask_wtf import Form
from wtforms import StringField, validators

class WordForm(Form):
    target = StringField('target', [validators.Required()])
    clue = StringField('clue')
