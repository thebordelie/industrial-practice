from abc import abstractmethod, ABC
from typing import Optional
from model.establishment import Establishment


class DataProvider(ABC):

    # todo psql connect or orm
    def __init__(self, username: str, password: str, host: str, port: int, database: str):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    @abstractmethod
    def get_data(self) -> list[Establishment]: pass

    @abstractmethod
    def add_data(self, establishment: Establishment): pass
