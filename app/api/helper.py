import pandas as pd
import io


def serialize_data_frame(df):
    # print("Returning: ", type(df.T.values().to_list()))
    try:
        return list(df.T.to_dict().values())
    except Exception as e:
        print("DF Serializer crashed: ", e)


def check_data_type(data):
    return str(type(data)).split(" ")[-1].split("'")[1].split(".")[-1].lower()


def generate_dataframe(raw_data):
    df = pd.read_csv(io.StringIO(raw_data.decode('utf-8')))
    df.fillna("", inplace=True)
    return df

