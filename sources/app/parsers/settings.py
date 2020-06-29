import os

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
    def search_engines(self):
        return self.config.get('search_engine')

    @property
    def keywords(self):
        return self.config.get('keyword')

    @property
    def to_emails(self):
        return self.config.get('to_email')
