from typing import List


class BaseParser:
    @staticmethod
    def parse(results: List[dict], **kwargs):
        """
        results 를 가지고 원하는 형식으로 변경하여 리턴해주세요
        """
        raise NotImplementedError('BaseParser 를 상속하면 parse 메서드를 구현해야합니다.')
