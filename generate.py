from faker import Faker
from faker.providers import internet


class DataGenerator:

    def __init__(self):
        self.fake = Faker()
        self.__initialize__()

    def __initialize__(self):
        # self.fake.add_provider(internet)
        pass

    def generate(self, meta: dict, n=100):
        print(self.fake.ean())


datagen = DataGenerator()
datagen.generate({'code': ''}, 100)
