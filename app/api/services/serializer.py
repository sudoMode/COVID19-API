import io
import pandas as pd
import json
from app.api import helper


SERIALIZATION_MAP = {
    "dataframe": helper.serialize_data_frame
}


def response_maker(f):
    def func(*args, **kwargs):
        try:
            rv = f(*args, **kwargs)
            data_type = helper.check_data_type(rv[0])
            print("DTRV: ", data_type)
            serializer = SERIALIZATION_MAP.get(data_type)
            if serializer is not None:
                rv = serializer(rv[0]), rv[1]
            return rv
        except Exception as e:
            print("Wrapper crashed: ", e)
    return func






