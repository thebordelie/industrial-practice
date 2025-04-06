from service.recommender_system import RecommenderSystem
from model.recommendation_strategy import Strategy
from model.establishment import Establishment
from utils.config_parser import ConfigParser
import logging

logger = logging.getLogger(__name__)


class RecommendationService:
    def __init__(self, recommender_systems: list[RecommenderSystem]):
        self.recommender_systems = {}
        self.current_strategy = Strategy(ConfigParser.get_attr("strategy"))
        for system in recommender_systems:
            self.recommender_systems[system.strategy] = system

    # todo dynamic strategy?
    def get_recommendations(self, user_id: int, count_of_establishments: int) -> list[
        Establishment]:
        logger.info(f"recommendations for {user_id}, count = {count_of_establishments}")
        return self.recommender_systems[self.current_strategy].get_recommendations(user_id, count_of_establishments)
