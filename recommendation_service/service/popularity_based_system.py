from model.establishment import Establishment
from model.recommendation_strategy import Strategy
from service.recommender_system import RecommenderSystem
from repository.establishment_repository import DataProvider


class PopularityBasedSystem(RecommenderSystem):

    def __init__(self, repository: DataProvider):
        super().__init__(Strategy.POPULARITY_BASED, repository)

    # todo performance
    def get_recommendations(self, user_id: int, count_of_establishments: int) -> list[Establishment]:
        establishments = self.repository.get_data()
        establishments.sort()
        return establishments[:count_of_establishments + 1]
