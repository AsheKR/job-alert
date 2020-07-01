from typing import List


class BaseParser:
    @staticmethod
    def parse(results: List[dict], **kwargs):
        raise NotImplementedError('BaseParser 를 상속하면 parse 메서드를 구현해야합니다.')
