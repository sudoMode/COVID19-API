from app.api import api
from app.api import extractor
from app.api import filter_args
from app.api import BaseHandler
from app.api import datetime as dt


ns = api.namespace('covid-19/confirmed', description='COVID-19 confirmed cases')


@ns.route(r"/")
class Confirmed(BaseHandler):

    CATEGORY_SUPPORTED = 'confirmed'

    def __init__(self, api=None):
        self.api = api
        super(Confirmed, self).__init__(api=self.api)
        self.__err = None

    def __validate_payload(self):
        # check columns
        if not self.__validate_payload__():
            raise ValueError('Payload Validation Failed!')

    def __parse_payload(self):
        try:
            self.__validate_payload()
            self.__pre_process_payload__()
            self.__serialize__(Confirmed.CATEGORY_SUPPORTED)
        except Exception as e:
            print('Data Parser Crashed: ', e)

    @api.expect(filter_args)
    def get(self):
        try:
            # try and check if data is to be pulled again
            update_is_needed = self.__update_check__(Confirmed.CATEGORY_SUPPORTED)
            if update_is_needed:
                # load data into a csv file
                self.payload = extractor.global_data_extractor(Confirmed.CATEGORY_SUPPORTED)
                self.__parse_payload()
            else:
                print('Using existing data')
        except Exception as e:
            print("Get Confirmed Crashed: ", e)
        return self.payload, self.code

