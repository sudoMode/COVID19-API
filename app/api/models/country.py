from app.api.models import Base
from app.api.models import Region
# from app.api.models import Location
# from app.api.models import History


class Country(Base):

    LAST_CONFIRMATION_UPDATED = None
    LAST_DEATHS_UPDATED = None
    LAST_RECOVERY_UPDATED = None
    UPDATE_CHECK_MAP = {
                            'confirmed': LAST_CONFIRMATION_UPDATED,
                            'deaths': LAST_DEATHS_UPDATED,
                            'recovered': LAST_RECOVERY_UPDATED
                        }

    def __init__(self, name):
        super(Country, self).__init__(name)
        self.regional_data = {}

    def __repr__(self):
        return f'<COVID-19 Affected Country>: [ {self.name} ]'

    @staticmethod
    def __check_for_update__(category):
        last_updated = Country.UPDATE_CHECK_MAP.get(category)
        update_is_needed = False
        if last_updated is None:
            print('fresh request is needed')
            update_is_needed = True
        else:
            print('last_updated was not None this time')
            pass
        return update_is_needed

    def __load_regional_data(self, data):
        try:
            available_regions = list(filter(lambda x: x != '', data.province_state.unique()))
            print('here: ', available_regions)
            # if regional_data_is_available:
            #     for i, row in data.iterrows():
            #         region = Region(row.province_state)
            #         region.__load_confirmation_data__(row)
            #         self.regional_data[region.name] = region
        except Exception as e:
            print('Regional Data Failed: ', e)

    def __validate_data(self, data):
        if not self.__validate_data__(data):
            raise ValueError(f'Data validation failed because: {self.msg}')

    def __load_confirmation_data__(self, data):
        try:
            self.__validate_data(data)
            self.__load_confirmed_data__(data)
            # self.__load_regional_data(data)
        except Exception as e:
            print('Confirm loader failed: ', e)
            return False

    def __load_deaths_data__(self, data):
        pass

    def __load_recovery_data__(self, data):
        pass
