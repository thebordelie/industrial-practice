from random import random
from repository.establishment_repository import DataProvider
from model.establishment import Establishment


class TestDataProvider(DataProvider):
    def __init__(self):
        super().__init__('url', 'login', 'password')
        self.establishments = []
        for i in range(100):
            self.establishments.append(
                Establishment("name" + str(i), "description" + str(i), "address" + str(i), random() * 9 + 1))

    def get_data(self) -> list[Establishment]:
        return self.establishments

    def add_data(self, establishment: Establishment):
        self.establishments.append(establishment)

