import os
from typing import List

import yaml


class ParseSettings:
    BASE_TARGET_PATH = os.path.dirname((os.path.abspath(__file__)))
    TARGET_FILE = 'settings.yaml'

    def __init__(self, target_website):
        self.target_website = target_website

        self._config = []

    @property
    def config(self) -> dict:
        if not self._config:
            target_path = os.path.join(self.BASE_TARGET_PATH, self.TARGET_FILE)

            if not os.path.exists(target_path):
                return {}

            with open(target_path, 'r') as target_file:
                config = yaml.load(target_file, Loader=yaml.SafeLoader)

            self._config = config.get(self.target_website)

        return self._config

    @property
    def keywords(self) -> List[str]:
        return self.config.get('keywords')
