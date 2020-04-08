class History:

    def __init__(self, history_type):
        self.type = 'country_wise' if history_type == 'country' else 'regional'
        self.distribution = None

    def __load(self, data):
        target_column = data.columns[0]
        print('Tk ', target_column)

    def __load_new_data__(self, data):
        rows, columns = data.shape
        for i in range(columns):
            column = data.iloc[:, i:i+1]
            self.__load(column)
            # break


