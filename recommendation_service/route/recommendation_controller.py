from repository.test_repository import TestDataProvider
from service.popularity_based_system import PopularityBasedSystem
from service.recommedation_service import RecommendationService
from flask import Flask, jsonify, request
import logging

logger = logging.getLogger(__name__)

test_data_provider = TestDataProvider()  # todo replace it with a normal provider
popularity_based_system = PopularityBasedSystem(test_data_provider)
recommendation_service = RecommendationService([popularity_based_system])  # todo add others recomm services

app = Flask(__name__)


@app.route('/establishments/<int:user_id>', methods=['GET'])
def get_recommendations(user_id):
    result = recommendation_service.get_recommendations(user_id, 10)
    recommendations = [item.to_json() for item in result]
    return jsonify(recommendations)


@app.route('/establishments', methods=['POST'])
def add_establishments():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json = request.json
        return 'ok'
    else:
        return 'Content-Type not supported!'


def run_app():
    logger.info('Started')
    app.run(debug=True)
