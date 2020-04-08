from app.api import api
from app.api import Resource
from app.api import extractor


ns = api.namespace('covid-19/recovered', description='COVID-19 recovered cases')


@ns.route(r"/")
class Recovery(Resource):

    def get(self):
        data = extractor.get_categorical_data("Recovered")
        return data
