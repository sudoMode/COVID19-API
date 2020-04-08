import requests
from pandas import read_csv
from io import StringIO


base_url = r"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/{}"
time_series_url = r"csse_covid_19_time_series/time_series_covid19_{}_global.csv"
daily_report_url = r"csse_covid_19_daily_reports/{}.csv"

url_map = {
    "time_series": base_url.format(time_series_url),
    "daily_report": base_url.format(daily_report_url)
}


def global_data_extractor(category):
    data = None
    url = url_map.get("time_series").format(category.lower())
    try:
        # extract data
        if url is not None:
            response = requests.get(url)
            if response.status_code == 200:
                data = read_csv(StringIO(response.content.decode('utf-8')))
    except ConnectionError as e:
        print("Detected Connection problem: ", e)
    except Exception as e:
        print('Get Data Error: ', e)
    return data







