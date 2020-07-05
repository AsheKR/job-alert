from datetime import datetime

from crawlers.rocket_punch import RocketPunchCrawler
from crawlers.wanted import WantedCrawler
from parsers.results import HTMLResultParser
from parsers.settings import SettingParser
from schemas import TYPE_ROCKET_PUNCH, TYPE_WANTED
from schemas.company import RocketPunchCompanySchema, WantedCompanySchema
from senders.html import HTMLDebugOutputSender
from senders.send_grid import SendGrid

SEARCH_ENGINES = {
    TYPE_ROCKET_PUNCH: {
        'label': '로켓펀치',
        'crawler': RocketPunchCrawler,
        'schema': RocketPunchCompanySchema,
    },
    TYPE_WANTED: {
        'label': '원티드',
        'crawler': WantedCrawler,
        'schema': WantedCompanySchema,
    },
}

SENDERS = {
    'html_output': {
        'label': 'HTML',
        'sender': HTMLDebugOutputSender,
        'parser': HTMLResultParser,
    },
    'send_grid': {
        'label': '이메일 ( SENDGRID )',
        'sender': SendGrid,
        'parser': HTMLResultParser,
    },
}


def main():
    settings = SettingParser()

    available_search_engines = settings.search_engines.keys()
    available_senders = settings.senders.keys()
    users = settings.users

    results = []

    for user in users:
        search_engines = user.get('search_engines').keys()
        senders = user.get('senders')
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

                if 'debug' in available_search_engines:
                    new_companies = crawler.companies

                    result['count'] += len(new_companies)
                    schema = SEARCH_ENGINES[search_engine]['schema'](many=True)
                    result['sites'].append({
                        'type': SEARCH_ENGINES[search_engine]['label'],
                        'count': len(new_companies),
                        'companies': schema.load(new_companies)
                    })
                else:
                    new_companies = crawler.get_new_companies()

                    if new_companies:
                        result['count'] += len(new_companies)
                        schema = SEARCH_ENGINES[search_engine]['schema'](many=True)
                        result['sites'].append({
                            'type': SEARCH_ENGINES[search_engine]['label'],
                            'count': len(new_companies),
                            'companies': schema.load(new_companies)
                        })

                    # TODO: 문제가 있다면 실패해도 기록하게 된다는 점?
                    crawler.write_latest_company_id_to_file()
            results.append(result)

        if sum(result['count'] for result in results):
            if 'debug' in available_senders:
                sender = SENDERS['html_output']['sender'](result_parser=SENDERS['html_output']['parser'])
                sender.prepare_data(results, title=f'{datetime.now().month}월 {datetime.now().day}일 Daily Haxim')
                sender.send()
            else:
                for sender, options in senders.items():
                    if sender not in available_senders:
                        raise ValueError(
                            f'{sender} 전송 방식은 제공되지 않습니다.\n'
                            f'제공 목록: [{",".join(available_senders)}]'
                        )

                    sender = SENDERS[sender]['sender'](options={**options, **settings.senders[sender]},
                                                       result_parser=SENDERS[sender]['parser'])
                    sender.prepare_data(results, title=f'{datetime.now().month}월 {datetime.now().day}일 Daily Haxim')
                    sender.send()


if __name__ == '__main__':
    main()
