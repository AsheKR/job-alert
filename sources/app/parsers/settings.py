import os
from typing import List

import yaml


class SettingParser:
    BASE_TARGET_PATH = os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__)))))
    TARGET_FILE = 'settings.yaml'

    def __init__(self):
        self._config = []

    @property
    def config(self) -> dict:
        if not self._config:
            target_path = os.path.join(self.BASE_TARGET_PATH, self.TARGET_FILE)

            if not os.path.exists(target_path):
                raise ValueError(f'{self.BASE_TARGET_PATH} 에 {self.TARGET_FILE} 파일이 존재하지 않습니다.')

            with open(target_path, 'r') as target_file:
                self._config = yaml.load(target_file, Loader=yaml.SafeLoader)

        return self._config

    @property
    def extensions(self) -> dict:
        return self.config.get('extensions')

    @property
    def search_engines(self) -> dict:
        return self.extensions.get('search_engines')

    @property
    def senders(self) -> dict:
        return self.extensions.get('senders')

    @property
    def users(self) -> List[dict]:
        return self.config.get('users')
