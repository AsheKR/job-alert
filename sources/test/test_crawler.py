from unittest import TestCase

from sources.crawler.rocket_punch import RocketPunchCrawler


class TestRockPunchCrawler(TestCase):

    def test_extend_query_string(self):
        rocket_punch = RocketPunchCrawler()
        assert len(rocket_punch.query_string) == 1

        rocket_punch.extend_query_string(['test'])
        assert len(rocket_punch.query_string) == 2
