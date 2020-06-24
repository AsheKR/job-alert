from typing import List


class RocketPunchCrawler:
    BASE_URL = 'https://www.rocketpunch.com/api/jobs/template'

    def __init__(self, query_string: List[str] = None):
        if query_string is None:
            query_string = []
        self.query_string = [('sort', 'recent')]
        self.extend_query_string(query_string)

    def extend_query_string(self, query_string: List[str]):
        self.query_string.extend([('keywords', keyword) for keyword in query_string])
