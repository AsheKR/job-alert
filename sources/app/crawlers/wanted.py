import os
from typing import List, Union

import requests
from requests import Response

from crawlers import BaseCrawler


class WantedCrawler(BaseCrawler):
    BASE_URL = 'https://www.wanted.co.kr'
    SEARCH_PATH = '/api/v4/search/summary'
    DETAIL_PATH = '/api/v4/jobs/{id}'

    BASE_TARGET_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'targets')
    TARGET_FILE_NAME = 'latest_wanted_id.txt'

    DEFAULT_QUERY_STRING: List[tuple] = [
        ('job_sort', 'job.latest_order'),
        ('locations', 'all'),
        ('years', '-1'),
        ('country', 'kr'),
    ]
    KEYWORD_NAME: str = 'query'

    def get_companies(self) -> List[dict]:
        response = self.get_response()
        json = response.json()
        jobs = json.get('jobs').get('data')

        companies = []

        for job in jobs:
            detail_response = self.get_detail_response(job.get('id'))
            job['detail'] = detail_response.json()
            companies.append(WantedCrawler.parse_company(job))

        return companies

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

    def get_detail_response(self, company_id: Union[str, int]):
        response = requests.get(self.BASE_URL + self.DETAIL_PATH.format(id=company_id))

        if not response.status_code == 200:
            raise ValueError(
                f'결과를 가져오는데 실패했습니다.\n'
                f'StatusCode: {response.status_code}\n'
                f'response: {response.raw}'
            )

        return response

    @classmethod
    def parse_company(cls, job: dict) -> dict:
        job_details = [cls.parse_job_detail(job)]

        return {
            'id': job.get('id'),
            'url': job.get('detail').get('job').get('short_link'),
            'logo_url': job.get('logo_img').get('thumb'),
            'name': job.get('company').get('name'),
            'description': '',
            'meta': [tag.get('title') for tag in job.get('detail').get('job').get('company_tags')],

            'industry_name': job.get('company').get('industry_name'),
            'response_avg_rate': job.get('company').get('application_response_stats').get('avg_rate'),
            'response_level': job.get('company').get('application_response_stats').get('level'),
            'response_delayed_count': job.get('company').get('application_response_stats').get('delayed_count'),
            'response_avg_day': job.get('company').get('application_response_stats').get('avg_day'),
            'response_remained_count': job.get('company').get('application_response_stats').get('remained_count'),
            'response_type': job.get('company').get('application_response_stats').get('type'),
            'address': job.get('detail').get('job').get('address').get('full_location'),
            'like_count': job.get('like_count'),

            'images': [item.get('url') for item in job.get('detail').get('job').get('company_images')],
            'job_details': job_details,
        }

    @classmethod
    def parse_job_detail(cls, job: dict) -> dict:
        meta = [f'{job.get("due_time")} 마감'] if job.get('due_time') else []

        return {
            'id': job.get('id'),
            'url': job.get('detail').get('job').get('short_link'),
            'title': job.get('position'),
            'meta': meta,

            'formatted_total': job.get('detail').get('job').get('reward').get('formatted_total'),
            'formatted_recommender': job.get('detail').get('job').get('reward').get('formatted_recommender'),
            'formatted_recommendee': job.get('detail').get('job').get('reward').get('formatted_recommendee'),
            'requirements': job.get('detail').get('job').get('detail').get('requirements'),
            'main_tasks': job.get('detail').get('job').get('detail').get('main_tasks'),
            'intro': job.get('detail').get('job').get('detail').get('intro'),
            'benefits': job.get('detail').get('job').get('detail').get('benefits'),
            'preferred_points': job.get('detail').get('job').get('detail').get('preferred_points'),
        }
