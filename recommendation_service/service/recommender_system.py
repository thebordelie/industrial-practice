from abc import abstractmethod, ABC

from model.recommendation_strategy import Strategy
from model.establishment import Establishment
from repository.establishment_repository import DataProvider


class RecommenderSystem(ABC):
    def __init__(self, strategy: Strategy, repository: DataProvider):
        self.strategy = strategy
        self.repository = repository

    @abstractmethod
    def get_recommendations(self, user_id: int, count_of_establishments: int) -> list[Establishment]: pass
