import os
from typing import List

import requests
from bs4 import BeautifulSoup, Tag
from requests import Response


class RocketPunchCrawler:
    BASE_URL = 'https://www.rocketpunch.com/api/jobs/template'
    BASE_TARGET_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'targets')
    TARGET_FILE = 'latest_rocket_punch_id.txt'

    def __init__(self, keywords: List[str] = None):
        # inner Controlled Data
        self._file_data = []
        self._companies = []
        self._keywords = []

        if keywords is None:
            keywords = []

        self.query_string = [('sort', 'recent')]
        self.extend_keywords(keywords)

    @property
    def keywords(self) -> List[str]:
        return self._keywords

    @property
    def file_data(self) -> List[str]:
        if not self._file_data:
            target_path = os.path.join(self.BASE_TARGET_PATH, self.TARGET_FILE)

            if not os.path.exists(target_path):
                return []

            with open(target_path, 'r') as target_file:
                self._file_data = target_file.readlines()

        return self._file_data

    @property
    def companies(self) -> List[dict]:
        if not self._companies:
            response = self.get_response()
            html = self.parse_html_from_response(response)
            self._companies = self.parse_html(html)

        return self._companies

    def extend_keywords(self, keywords: List[str]) -> None:
        self._keywords.extend(keywords)
        self.query_string.extend([('keywords', keyword) for keyword in keywords])

    def get_new_companies(self) -> List[dict]:
        latest_company_id_from_file = self.get_latest_company_id_from_file()
        latest_company_id_from_api = self.get_latest_company_id_from_api()

        # 첫 크롤링 시
        if not latest_company_id_from_file:
            return []

        # 업데이트가 없을 시
        if latest_company_id_from_file == latest_company_id_from_api:
            return []

        new_companies = []

        for company in self.companies:
            # ID 가 동일한 것이 있을 때까지 신규 등록 공고.
            if company.get('company_id') == latest_company_id_from_file:
                break
            new_companies.append(company)

        return new_companies

    def write_latest_company_id_to_file(self) -> None:
        latest_company_id = self.get_latest_company_id_from_api()
        target_path = os.path.join(self.BASE_TARGET_PATH, self.TARGET_FILE)
        target_string = f'{",".join(self.keywords)}:{latest_company_id}'

        file_data = self.file_data.copy()

        for index, line in enumerate(file_data):
            if line.startswith(','.join(self.keywords)):
                file_data[index] = target_string
                break
        else:
            file_data.append(target_string)

        with open(target_path, 'w') as target_file:
            target_file.write('\n'.join(file_data))

    def get_latest_company_id_from_file(self) -> str:
        data = self.file_data

        for line in data:
            if line.startswith(','.join(self.keywords)):
                latest_company_id = line.split(':')[1]
                break
        else:
            latest_company_id = ''

        return latest_company_id

    def get_latest_company_id_from_api(self) -> str:
        if not self.companies:
            raise ValueError(
                f'크롤러로 가져온 결과가 존재하지 않습니다.'
            )

        return self.companies[0].get('company_id')

    def get_response(self) -> Response:
        response = requests.get(self.BASE_URL, params=self.query_string)

        if not response.status_code == 200:
            raise ValueError(
                f'결과를 가져오는데 실패했습니다.\n'
                f'StatusCode: {response.status_code}\n'
                f'response: {response.raw}'
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

    @staticmethod
    def parse_company(soup_company: Tag) -> dict:
        company_id = soup_company.attrs.get('data-company_id')
        company_url = soup_company.select_one('.logo.image > a').attrs.get('href')
        logo_url = soup_company.select_one('.logo.image > a > .ui.logo > img.ui.image').attrs.get('src')
        name = soup_company.select_one('.content > .company-name > a > h4.header.name > strong').text

        sub_name = getattr(soup_company.select_one('.content > .company-name > a > h4.header.name > small'), 'text', '')
        thumb_up_count = getattr(soup_company.select_one('.content > .company-name > a.reference-count > span.count'),
                                 'text', '')

        description = getattr(soup_company.select_one('.content > .description'), 'text', '')

        # TODO: Split Meta Tag
        meta = getattr(soup_company.select_one('.content > .meta'), 'text', '').strip()

        # get parsed job details
        soup_job_details = soup_company.select('.content > .company-jobs-detail > .job-detail')
        job_details = []
        for soup_job_detail in soup_job_details:
            job_details.append(RocketPunchCrawler.parse_job_detail(soup_job_detail))

        return {
            'company_id': company_id,
            'company_url': company_url,
            'logo': logo_url,
            'name': name,
            'sub_name': sub_name,
            'thumb_up_count': thumb_up_count,
            'description': description,
            'meta': meta,
            'job_details': job_details,
        }

    @staticmethod
    def parse_job_detail(soup_job_detail: Tag) -> dict:
        job_detail_id = soup_job_detail.select_one('.job-title').attrs.get('href').split('/')[2]
        url = soup_job_detail.select_one('.job-title').attrs.get('href')
        title = soup_job_detail.select_one('.job-title').text

        # TODO: Classification meta tag
        job_detail_date_meta_1 = getattr(soup_job_detail.select_one('.job-dates > span:nth-child(1)'), 'text', '').strip()
        job_detail_date_meta_2 = getattr(soup_job_detail.select_one('.job-dates > span:nth-child(2)'), 'text', '').strip()

        return {
            'job_detail_id': job_detail_id,
            'url': url,
            'title': title,
            'job_detail_date_meta_1': job_detail_date_meta_1,
            'job_detail_date_meta_2': job_detail_date_meta_2,
        }
