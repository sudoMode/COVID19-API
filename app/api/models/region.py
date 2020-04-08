from app.api.models import Base


class Region(Base):

    def __init__(self, name):
        super(Region, self).__init__(name)

    def __load_confirmation_data__(self, data):
        try:
            # print('Region: ', self.name + 'here')
            # print('Data: ', data)
            pass
        except Exception as e:
            print('Region loader: '. e)