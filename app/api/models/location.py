from app.api.models import re
from app.api.models import History


class Location:

    def __init__(self, name, location_type):
        self.name = name
        self.type = location_type
        self.latitude = None
        self.longitude = None
        self.confirmation_history = None
        self.death_history = None
        self.recovery_history = None
        self.__last_update_date = None
        self.__last_update_rows = 0

    def __set_latitude(self, value):
        self.latitude = value

    def __set_longitude(self, value):
        self.longitude = value

    def __update_coordinates(self, data):
        latitude = data.lat.mean() if data.shape[0] > 1 else data.lat.values[0]
        longitude = data.long.mean() if data.shape[0] > 1 else data.long.values[0]
        if self.latitude != latitude:
            self.__set_latitude(latitude)
        if self.longitude != longitude:
            self.__set_longitude(longitude)

    @staticmethod
    def __get_date_columns(data):
        # separate out the data for dates
        headers_in_a_string = '|'.join(data.columns)
        date_like_pattern = r'(\d{1,2}_\d{1,2}_\d{1,4})'
        available_dates = re.findall(date_like_pattern, headers_in_a_string)
        return available_dates

    @staticmethod
    def __get_columns_to_load(fresh_data, existing_history):
        if existing_history is None:
            return fresh_data.columns
        else:
            return fresh_data.columns

    @staticmethod
    def __check_if_rows_have_been_updated(data, existing_history):
        return data.shape[0] > existing_history.shape[0]

    @staticmethod
    def __check_if_columns_have_been_updated(data, existing_history):
        return data.shape[1] > existing_history.shape[1]

    @staticmethod
    def __check_for_new_data(data, existing_history):
        rows_to_be_updated = Location.__check_if_rows_have_been_updated(data, existing_history)
        columns_to_be_updated = Location.__check_if_columns_have_been_updated(data, existing_history)
        return rows_to_be_updated or columns_to_be_updated

    @staticmethod
    def __check_if_update_is_needed(data, existing_history):
        # data has not been loaded previously
        if existing_history is None:
            check_status = True
        else:
            # if data already exists
            check_status = Location.__check_for_new_data(data, existing_history)
        return check_status

    @staticmethod
    def __get_columns_to_update(data, existing_history):
        # return only those columns that are new
        if existing_history is None:
            column_start, column_end = 0, data.shape[1]
        else:
            column_start, column_end = existing_history.shape[1], data.shape[1]
        return data.iloc[:, column_start:column_end]

    @staticmethod
    def __get_rows_to_update(data, existing_history):
        # return only those rows that new
        if existing_history is None:
            row_start, column_start, column_end = 0, 0, data.shape[1]
        else:
            print('Getting data by i loc')
            row_start, column_start, column_end = existing_history.shape[0], 0, existing_history.shape[1]
        return data.iloc[row_start:, column_start:column_end]

    @staticmethod
    def __get_new_historical_data(data):
        available_dates = Location.__get_date_columns(data)
        data = data[available_dates]
        return data

    def __update_column_wise_features(self, data, existing_history):
        if existing_history is None:
            existing_history = History(self.type)

    def __update_row_wise_features(self, data, existing_history):
        if existing_history is None:
            existing_history = History(self.type)
        existing_history.__load_new_data__(data)

    def __update_history(self, data, history_type):
        history_map = {
                            'confirmed': self.confirmation_history,
                            'deaths': self.death_history,
                            'recovered': self.recovery_history
                        }
        try:
            existing_history = history_map.get(history_type)
            new_historical_data = Location.__get_new_historical_data(data)
            update_is_needed = Location.__check_if_update_is_needed(new_historical_data, existing_history)
            if update_is_needed:
                rows_to_be_updated = Location.__get_rows_to_update(new_historical_data, existing_history)
                if rows_to_be_updated is not None:
                    self.__update_row_wise_features(rows_to_be_updated, existing_history)
                columns_to_be_updated = Location.__get_columns_to_update(new_historical_data, existing_history)
                if columns_to_be_updated is not None:
                    self.__update_column_wise_features(columns_to_be_updated, existing_history)

        except Exception as e:
            print('History Loader Crashed: ', e, self.name)

    def __load_data__(self, data, category):
        try:
            self.__update_coordinates(data)
            self.__update_history(data, category)

        except Exception as e:
            print('Data Loader Crashed: ', e, self.name)
