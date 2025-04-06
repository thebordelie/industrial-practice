from route.recommendation_controller import run_app
import logging

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    run_app()
