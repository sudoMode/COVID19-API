from flask import Flask
from app.api import api
from app.api import blueprint
from app.api.endpoints.deaths import ns as death_namespace
from app.api.endpoints.recovered import ns as recovered_namespace
from app.api.endpoints.confirmed import ns as confirmed_namespace


app = Flask(__name__)