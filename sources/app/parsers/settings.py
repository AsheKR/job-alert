import os

import yaml


class ParseSettings:
    BASE_TARGET_PATH = os.path.dirname((os.path.abspath(__file__)))
    TARGET_FILE = 'settings.yaml'

    def __init__(self):
        self._config = []

    @property
    def config(self) -> dict:
        if not self._config:
            target_path = os.path.join(self.BASE_TARGET_PATH, self.TARGET_FILE)

            if not os.path.exists(target_path):
                return {}

            with open(target_path, 'r') as target_file:
                self._config = yaml.load(target_file, Loader=yaml.SafeLoader)

        return self._config
