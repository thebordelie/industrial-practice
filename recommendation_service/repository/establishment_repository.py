from abc import abstractmethod, ABC
from typing import Optional
from model.establishment import Establishment


class DataProvider(ABC):

    # todo psql connect or orm
    def __init__(self, url: str, login: Optional[str], password: Optional[str]):
        self.url = url
        self.login = login
        self.password = password

    @abstractmethod
    def get_data(self) -> list[Establishment]: pass

    @abstractmethod
    def add_data(self, establishment: Establishment): pass
