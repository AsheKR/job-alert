from adapters.rocket_punch import RocketPunchAdapter
from crawlers.rocket_punch import RocketPunchCrawler
from parsers.company import CompanyParser
from parsers.settings import SettingParser


def main():
    settings = SettingParser()
    keywords = settings.config.get('rocket_punch').get('keywords')

    synthesis_result = ''

    for keyword in keywords:
        rocket_punch = RocketPunchCrawler(keywords=keyword.split(','))
        companies = rocket_punch.get_new_companies()
        if companies:
            synthesis_result += f'{keyword}'
            synthesis_result += '<hr />'
            adapter = RocketPunchAdapter(companies, CompanyParser)
            synthesis_result += adapter.to_html()
        rocket_punch.write_latest_company_id_to_file()


if __name__ == "__main__":
    main()
