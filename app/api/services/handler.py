from app.api import helper
from app.api import Resource
from app.api import datetime as dt
from app.api.models import Country
from app.api.models import serializer
from app.api import re


class BaseHandler(Resource):
    DEFAULT_ERR_MSG = 'bad response from server'
    DEFAULT_STATUS_CODE = 500
    # to match: [ Province/State|Country|Region|Lat|Long|1/1/20|1/2/20 and so on ....> ]
    EXPECTED_HEADER_PATTERN = r'((P\w+\/S\w+)\|(C\w+\/R\w+)\|(L\w+)\|(L\w+)\|(\d{1,2}\/\d{1,2}\/\d{1,4}\|*)+)'

    def __init__(self, api=None):
        super(BaseHandler, self).__init__(api=api)
        self.__err = False
        self.msg = None
        self.code = None
        self.payload = None
        self.metadata = None
        self.status = None
        self.response = None
        self.data = None
        self.last_updated = None
        self.__set_defaults()

    def __set_defaults(self):
        self.msg = BaseHandler.DEFAULT_ERR_MSG
        self.code = BaseHandler.DEFAULT_STATUS_CODE
        self.payload = {"error": self.__err}
        self.metadata = {}
        self.status = 'OK'
        self.response = self.payload

    def __validate_headers(self):
        expected_header_pattern = BaseHandler.EXPECTED_HEADER_PATTERN
        try:
            headers_in_a_string = '|'.join(self.payload.columns)
            match_was_found = re.match(expected_header_pattern, headers_in_a_string)
            if not match_was_found:
                raise ValueError('Payload headers did not match the expected pattern.')
        except Exception as e:
            self.__err = True
            self.msg = e

    def __validate_data_types(self):
        try:
            raise NotImplementedError('Data type validation is not implemented yet.')
        except Exception as e:
            # self. __err = True
            self.msg = e

    def __validate_payload__(self):
        self.__validate_headers()
        self.__validate_data_types()
        validation_status = not self.__err
        return validation_status

    def __validate_response(self):
        acceptable_response_types = ["str", "list", "dict"]
        response_type = helper.check_data_type(self.payload)
        return response_type in acceptable_response_types

    def __pre_process_payload__(self):
        try:
            self.payload.fillna('', inplace=True)
            self.payload.columns = list(map(lambda x: x.lower().replace('/', '_'), self.payload.columns))
            self.payload.country_region = self.payload.country_region.apply(lambda x: str(x).lower().replace(' ', '_'))
            self.payload.province_state = self.payload.province_state.apply(lambda x: str(x).lower().replace(' ', '_'))
        except Exception as e:
            self.__err = True
            self.msg = f'Pre-processor failed: [ {e} ]'

    def __set_last_updated_date__(self, date):
        expected_format = '%m_%d_%y'
        self.last_updated = dt.strptime(date, expected_format)

    @staticmethod
    def __update_check__(category):
        update_is_needed = Country.__check_for_update__(category)
        return update_is_needed

    def __serialize__(self, category):
        # make payload presentable
        if self.__err:
            self.msg = f'Serialization failed because: {self.msg}'
            raise ValueError(self.msg)
        self.payload = serializer.serialize_raw_data(self.payload, category)

