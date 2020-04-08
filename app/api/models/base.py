from app.api.models import Location


class Base(object):

    def __init__(self, name):
        self.name = name
        self.total_confirmed = 0
        self.total_dead = 0
        self.total_recovered = 0
        self.location = None
        self.latest_data_date = None
        self.__err = False
        self.msg = ''

    @staticmethod
    def __get_data_type(data):
        return str(type(data)).split('.')[-1][:-2].lower()

    def __validate_data__(self, data):
        try:
            data_type = Base.__get_data_type(data)
            if data_type == 'dataframe':
                countries_available = data.country_region.unique()
                total_countries_available = len(countries_available)
                if bool(total_countries_available):
                    if total_countries_available > 1 or self.name != countries_available[0]:
                        raise ValueError(f'Request was made to load data for "{self.name}"'
                                         f', but data was supplied for: "{countries_available}"')
                else:
                    raise ValueError(f'Request was made to load data for "{self.name}", '
                                     f'but there was no data to load from :(')
            else:
                raise ValueError(f'Data was supplied in a {data_type} format, only "dataframes" are supported')
        except Exception as e:
            self.__err = True
            self.msg = e
        validation_status = not self.__err
        return validation_status

    # def __get_columns_to_load(self, data):
    #     not used yet
        # if self.__confirmed_data is None:
        #     return data.columns
        # else:
        #     return data.columns[len(self.__confirmed_data.columns):]

    def __parse_confirmed(self, data):
        try:
            if self.location is None:
                self.location = Location(self.name, 'country')
            self.location.__load_data__(data, 'confirmed')

        except Exception as e:
            print('Confirmed Parser Failed: ', e)

    def __load_confirmed_data__(self, data):
        try:
            self.__parse_confirmed(data)

            pass
        except Exception as e:
            self.__err = True
            self.msg = e
            print('Base Confirmation Loader Failed: ', e)
            return


