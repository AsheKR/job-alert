import os
from typing import List

import requests
from bs4 import BeautifulSoup, Tag
from requests import Response

from crawlers import BaseCrawler


class RocketPunchCrawler(BaseCrawler):
    BASE_URL = 'https://www.rocketpunch.com'
    SEARCH_PATH = '/api/jobs/template'

    BASE_TARGET_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'targets')
    TARGET_FILE_NAME = 'latest_rocket_punch_id.txt'

    # 기본 제공할 query_string 이 존재하는 경우 지정한다.
    DEFAULT_QUERY_STRING: List[tuple] = [('sort', 'recent')]
    KEYWORD_NAME: str = 'keywords'

    def get_companies(self) -> List[dict]:
        if not self._companies:
            response = self.get_response()
            html = self.parse_html_from_response(response)
            self._companies = self.parse_html(html)

        return self._companies

    def get_response(self) -> Response:
        response = requests.get(self.BASE_URL + self.SEARCH_PATH, params=self.query_string)

        if not response.status_code == 200:
            raise ValueError(
                f'결과를 가져오는데 실패했습니다.\n'
                f'StatusCode: {response.status_code}\n'
                f'response: {response.raw}\n'
                f'url: {self.BASE_URL}\n'
                f'params: {self.query_string}'
            )

        return response

    @staticmethod
    def parse_html_from_response(response: Response) -> str:
        json = response.json()
        data = json.get('data')
        template = data.get('template')

        return template

    @staticmethod
    def parse_html(html: str) -> List[dict]:
        soup = BeautifulSoup(html, 'html.parser')
        soup_companies = soup.select('div#company-list > .company.item')

        # get parsed Companies
        companies = []
        for soup_company in soup_companies:
            companies.append(RocketPunchCrawler.parse_company(soup_company))

        return companies

    @classmethod
    def parse_company(cls, soup_company: Tag) -> dict:
        company_id = soup_company.attrs.get('data-company_id')
        company_url = soup_company.select_one('.logo.image > a').attrs.get('href')
        logo_url = soup_company.select_one('.logo.image > a > .ui.logo > img.ui.image').attrs.get('src')
        name = soup_company.select_one('.content > .company-name > a > h4.header.name > strong').text

        sub_name = getattr(soup_company.select_one('.content > .company-name > a > h4.header.name > small'), 'text', '')
        thumb_up_count = getattr(soup_company.select_one('.content > .company-name > a.reference-count > span.count'),
                                 'text', 0) or 0

        description = getattr(soup_company.select_one('.content > .description'), 'text', '')

        # TODO: Split Meta Tag
        meta = getattr(soup_company.select_one('.content > .meta'), 'text', '').strip()

        # get parsed job details
        soup_job_details = soup_company.select('.content > .company-jobs-detail > .job-detail')
        job_details = []
        for soup_job_detail in soup_job_details:
            job_details.append(RocketPunchCrawler.parse_job_detail(soup_job_detail))

        return {
            'id': company_id,
            'url': cls.BASE_URL + company_url,
            'logo_url': logo_url,
            'name': name,
            'sub_name': sub_name,
            'thumb_up_count': thumb_up_count,
            'description': description,
            'meta': meta,
            'job_details': job_details,
        }

    @classmethod
    def parse_job_detail(cls, soup_job_detail: Tag) -> dict:
        job_detail_id = soup_job_detail.select_one('.job-title').attrs.get('href').split('/')[2]
        url = soup_job_detail.select_one('.job-title').attrs.get('href')
        title = soup_job_detail.select_one('.job-title').text

        job_stats_info = getattr(soup_job_detail.select_one('.job-stats-info'), 'text', '')

        # TODO: Classification meta tag
        job_detail_date_meta_1 = getattr(soup_job_detail.select_one('.job-dates > span:nth-child(1)'), 'text',
                                         '').strip()
        job_detail_date_meta_2 = getattr(soup_job_detail.select_one('.job-dates > span:nth-child(2)'), 'text',
                                         '').strip()

        return {
            'id': job_detail_id,
            'url': cls.BASE_URL + url,
            'title': title,
            'stats_info': job_stats_info,
            'meta': [job_detail_date_meta_1, job_detail_date_meta_2],
        }
