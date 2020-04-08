# used by other mods
from datetime import datetime
from datetime import timedelta
import re
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from flask_restplus import Resource


from flask_restplus import Api
from flask_restplus import reqparse
from flask import Blueprint
from app.api.services import extractor
from app.api.services import serializer
from app.api import helper
from app.api.services.handler import BaseHandler


api = Api(version='v1.0.0', title='COVID-19 API-dev', description='Test API')
blueprint = Blueprint('/api', __name__, url_prefix='/api')


filter_args = reqparse.RequestParser()
filter_args.add_argument(
                            'country_name',
                            type=str,
                            required=False,
                            help='Name of the country'
                        )
filter_args.add_argument(
                            'country_code',
                            type=str,
                            required=False,
                            help='Alpha-2 country code'
                        )
filter_args.add_argument(
                            'province',
                            type=str,
                            required=False,
                            help='Region of the country'
                        )