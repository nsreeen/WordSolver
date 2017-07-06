import sys
from flask import Flask

app = Flask(__name__)

app.secret_key = 'test'


from app import views

