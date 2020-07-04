import os
from typing import List, Optional


class BaseCrawler:
    """
    일관성있는 크롤러를 생성하기 위한 BaseCrawler
    """
    # 검색 할 URL 을 지정한다.
    BASE_URL: str = None
    SEARCH_PATH: str = None

    # 검색 후 최신 정보를 담아두기 위한 파일과 경로를 지정한다.
    BASE_TARGET_PATH: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'targets')
    TARGET_FILE_NAME: str = None

    # 기본 제공할 query_string 이 존재하는 경우 지정한다.
    DEFAULT_QUERY_STRING: List[tuple] = []
    KEYWORD_NAME: str = None

    def __init__(self, keywords: List[str] = None):
        assert self.BASE_URL is not None, (
            '크롤링 할 BASE_URL 을 제공해야 합니다.',
        )
        assert self.SEARCH_PATH is not None, (
            '검색 할 BASE_SEARCH_URL 을 제공해야 합니다',
        )
        assert self.TARGET_FILE_NAME is not None, (
            '저장 할 파일의 TARGET_FILE_NAME 을 제공해야 합니다.',
        )
        assert self.KEYWORD_NAME is not None, (
            '검색 시 키워드로 사용할 KEYWORD_NAME 을 제공해야 합니다.',
        )
        assert self.DEFAULT_QUERY_STRING is not None, (
            '정렬에 사용할 기본 DEFAULT_QUERY_STRING 을 제공해야 합니다.',
        )

        # inner Controlled Data
        self._keywords: List[str] = []
        self._file_data: List[str] = []
        self._companies: List[dict] = []

        if keywords is None:
            keywords = []

        self.extend_keywords(keywords)

    @property
    def keywords(self) -> List[str]:
        """
        검색 키워드를 가져오는 프로퍼티
        """
        return self._keywords

    @property
    def query_string(self) -> List[tuple]:
        """
        기본 설정과 함께 설정된 키워드를 가져오는 프로퍼티
        """
        return self.DEFAULT_QUERY_STRING + [(self.KEYWORD_NAME, keyword) for keyword in self.keywords]

    @property
    def file_data(self) -> List[str]:
        """
        파일에서 데이터를 읽어 가져오는 프로퍼티
        """
        if not self._file_data:
            target_path = os.path.join(self.BASE_TARGET_PATH, self.TARGET_FILE_NAME)

            if not os.path.exists(target_path):
                return []

            with open(target_path, 'r') as target_file:
                self._file_data = target_file.read().split('\n')

        return self._file_data

    @property
    def companies(self) -> List[dict]:
        """
        모든 크롤링한 회사 정보를 담고있는 프로퍼티
        """
        if not self._companies:
            self._companies = self.get_companies()

        return self._companies

    def extend_keywords(self, keywords: List[str]) -> None:
        """
        검색 키워드를 확장할 수 있게 도와주는 헬퍼
        """
        self._keywords.extend(keywords)

    def get_latest_company_id_from_file(self) -> Optional[int]:
        """
        이전에 검색한 결과 중 가장 최신의 ID 를 파일로부터 가져오는 메서드

        키워드 검색 시 해당 키워드의 최신 ID 를 파일에 기록하게 된다.
        해당 정보는 이전에 어디까지 크롤링했는지 확인하고 최신 정보만을 가져오기 위해 사용된다.
        """
        data = self.file_data

        for line in data:
            if line.startswith(','.join(self.keywords)):
                latest_company_id = line.split(':')[1]
                break
        else:
            latest_company_id = ''

        try:
            return int(latest_company_id)
        except ValueError:
            return None

    def get_latest_company_id_from_api(self) -> Optional[int]:
        """
        검색한 결과 중 가장 최신의 ID 를 가져오는 메서드
        """
        if not self.companies:
            raise ValueError(
                f'크롤러로 가져온 결과가 존재하지 않습니다.'
            )

        try:
            return self.companies[0].get('id')
        except ValueError:
            return None

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
            if int(company.get('id')) == latest_company_id_from_file:
                break
            new_companies.append(company)

        return new_companies

    def write_latest_company_id_to_file(self) -> None:
        """
        키워드 검색 결과의 최신 ID 를 기록하는 메서드

        키워드 검색 시 어디까지 크롤링했는지를 기록하기 위해 최신 ID 를 파일로 기록할 필요가 있다.
        이전에 키워드 검색이 있다면 해당 라인을 최신 ID 로 덮어쓴다.
        """
        latest_company_id = self.get_latest_company_id_from_api()
        target_path = os.path.join(self.BASE_TARGET_PATH, self.TARGET_FILE_NAME)
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

    def get_companies(self) -> List[dict]:
        raise NotImplementedError(
            'BaseCrawler 는 반드시 get_companies 를 구현해야합니다. '
            'Company 데이터는 CompanySchema 를 참고해서 구현해주세요.'
        )

    @classmethod
    def parse_company(cls, company: any) -> dict:
        """
        CompanySchema 를 참고하여 필요한 데이터를 채운 dict 를 리턴한다.
        """
        raise NotImplementedError(
            'BaseCrawler 는 반드시 parse_company 를 구현해야합니다. '
            'Company 데이터는 CompanySchema 를 참고해서 구현해주세요.'
        )

    @classmethod
    def parse_job_detail(cls, job_detail: any) -> dict:
        """
        JobSchema 를 참고하여 필요한 데이터를 채운 dict 를 리턴한다.
        """
        raise NotImplementedError(
            'BaseCrawler 는 반드시 parse_job_detail 를 구현해야합니다. '
            'Company 데이터는 JobDetailSchema 를 참고해서 구현해주세요.'
        )
