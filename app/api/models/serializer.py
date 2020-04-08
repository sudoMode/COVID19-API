from app.api.models import Country
from app.api import tqdm
from app.api import ThreadPoolExecutor
from app.api import partial
from time import sleep
from time import time



COUNTRY_MAP = {}


def get_unique_countries(data):
    return set(data.country_region)


def initialize_country(name):
    # create a country object and store it in a dictionary
    if name not in COUNTRY_MAP:
        country = Country(name)
        COUNTRY_MAP[name] = country
        return country


def initializer(data):
    # initialize and store an object for each country
    unique_countries = get_unique_countries(data)
    for every_country in unique_countries:
        initialize_country(every_country)


def get_executable(country, category):
    executable = None
    if category == 'confirmed':
        executable = country.__load_confirmation_data__
    if category == 'deaths':
        executable = country.__load_deaths_data__
    if category == 'recovered':
        executable = country.__load_recovery_data__
    return executable


def run_with_concurrent_threads(function):
    def wrapper(*args, **kwargs):
        max_workers = kwargs.get('max_workers') or 32
        try:
            with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix='Concurrent_Loader') as t:
                rv = list(t.map(partial(function, **kwargs), *args))
            return rv
        except Exception as e:
            print('Concurrent Runner Crashed: ', e)
    return wrapper


def timer(function):
    def wrapper(*args, **kwargs):
        start_time = time()
        rv = function(*args, **kwargs)
        end_time = time()
        time_lapsed = round(end_time - start_time, 2)
        print(f'********** Time Lapsed: [ {time_lapsed} seconds ] **********')
        return rv
    return wrapper


@timer
@run_with_concurrent_threads
def concurrent_loader(name, data, load_category):
    data_loader = get_executable(COUNTRY_MAP.get(name), load_category)
    relevant_data = data[data.country_region == name]
    data_load_was_complete = data_loader(relevant_data)
    sleep(0.5)
    # country = COUNTRY_MAP.get(name, initialize_country(name))
    # if country is not None:
    #     executable = get_executable(country, load_category)
    #     print('EXE: ', executable)
    pass


def serialize_confirmation_data(data, countries_to_load=None):
    # this function could be concurrent
    serialized_data = {}
    try:
        # countries_to_load = countries_to_load or COUNTRY_MAP.keys()
        countries_to_load = ['india', 'australia', 'kenya', 'japan', 'denmark', 'france']
        data = data[data.country_region.isin(countries_to_load)]
        concurrent_loader(countries_to_load, data=data, load_category='confirmed')
    except Exception as e:
        print('Confirmed data could not be serialized: ', e)
    return serialized_data


def serialize_death_data(data):
    pass


def serialize_recovery_data(data):
    pass


def serialize_raw_data(data, category):
    serialization_map = {
                            'confirmed': serialize_confirmation_data,
                            'deaths': serialize_death_data,
                            'recovered': serialize_recovery_data,
                        }
    initializer(data)
    serializer = serialization_map.get(category)
    serialized_data = serializer(data)
    print("just returning the same data back for now")
    serialized_data = list(data.T.to_dict().values())
    return serialized_data





