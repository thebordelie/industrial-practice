import configparser
import logging

logger = logging.getLogger(__name__)
config = configparser.RawConfigParser()
config.read(r"properties.txt")
details = dict(config.items('PROPERTIES'))


class ConfigParser:
    @staticmethod
    def get_attr(attribute_name: str):
        return details.get(attribute_name)
