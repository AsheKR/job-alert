from datetime import datetime

from crawlers.rocket_punch import RocketPunchCrawler
from crawlers.wanted import WantedCrawler
from parsers.results import HTMLResultParser
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

CHANNELS = {
    'send_grid': {
        'label': '이메일 ( SENDGRID )',
        'sender': SendGrid,
        'parser': HTMLResultParser,
    }
}


def get_results():
    settings = SettingParser()

    available_search_engines = settings.search_engines.keys()
    available_channels = settings.channels.keys()
    users = settings.users

    results = []

    for user in users:
        search_engines = user.get('search_engines').keys()
        channels = user.get('channels')
        keywords = user.get('keywords')

        for keyword in keywords:
            result = {
                'keyword': keyword,
                'count': 0,
                'sites': [],
            }

            for search_engine in search_engines:
                if search_engine not in available_search_engines:
                    raise ValueError(
                        f'{search_engine} 검색은 제공되지 않습니다.\n'
                        f'제공 목록: [{",".join(available_search_engines)}]'
                    )
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
                # crawler.write_latest_company_id_to_file()
            results.append(result)

        if sum(result['count'] for result in results):
            for channel, options in channels.items():
                if channel not in available_channels:
                    raise ValueError(
                        f'{channel} 전송 방식은 제공되지 않습니다.\n'
                        f'제공 목록: [{",".join(available_channels)}]'
                    )

                sender = CHANNELS[channel]['sender'](options={**options, **settings.channels[channel]}, result_parser=CHANNELS[channel]['parser'])
                sender.prepare_data(results, title=f'{datetime.now().month}월 {datetime.now().day}일 Daily Haxim')
                sender.send()


def main():
    get_results()


if __name__ == '__main__':
    main()
