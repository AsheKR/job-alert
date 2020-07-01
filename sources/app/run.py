from datetime import datetime

from jinja2 import Environment, FileSystemLoader

from crawlers.rocket_punch import RocketPunchCrawler
from crawlers.wanted import WantedCrawler
from parsers.settings import SettingParser
from schemas.company import CompanySchema
from senders.send_grid import SendGrid

SEARCH_ENGINES = {
    'rocket_punch': {
        'label': '로켓펀치',
        'crawler': RocketPunchCrawler,
    },
    'wanted': {
        'label': '원티드',
        'crawler': WantedCrawler,
    },
}


def get_results():
    settings = SettingParser()

    search_engines = settings.search_engines
    keywords = settings.keywords
    from_email = settings.from_email
    to_emails = settings.to_emails

    results = []

    for keyword in keywords:
        result = {
            'keyword': keyword,
            'count': 0,
            'sites': [],
        }

        for search_engine in search_engines:
            if not SEARCH_ENGINES.get(search_engine):
                raise ValueError(
                    f'{search_engine} 검색은 제공되지 않습니다.\n'
                    f'제공 목록: [{",".join(SEARCH_ENGINES.keys())}]'
                )
            crawler = SEARCH_ENGINES[search_engine]['crawler'](keywords=keyword.split(','))
            new_companies = crawler.get_new_companies()

            if new_companies:
                result['count'] += len(new_companies)
                schema = CompanySchema(many=True)
                result['sites'].append({
                    'type': SEARCH_ENGINES[search_engine]['label'],
                    'count': len(new_companies),
                    'companies': schema.load(new_companies)
                })

            # TODO: 문제가 있다면 실패해도 기록하게 된다는 점?
            crawler.write_latest_company_id_to_file()
        results.append(result)

    if sum(result['count'] for result in results):
        env = Environment(
            loader=FileSystemLoader(['templates', 'static']),
        )
        template = env.get_template('index.html')

        subject = f'{datetime.now().month}월 {datetime.now().day}일 Daily Haxim'

        html = template.render(
            title=subject,
            sub_title='일간 신규 채용 정보',
            results=results,
        )
        send_grid = SendGrid(from_email=from_email, to_email=to_emails)
        send_grid.send(subject=subject, content=html)


def main():
    get_results()


if __name__ == '__main__':
    main()
