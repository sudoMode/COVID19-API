from app.api import api
from app.api import Resource
from app.api import extractor


ns = api.namespace('covid-19/deaths', description='COVID-19 death cases')


@ns.route(r"/")
class Death(Resource):

    def get(self):
        data = extractor.get_categorical_data("Deaths")
        return data
