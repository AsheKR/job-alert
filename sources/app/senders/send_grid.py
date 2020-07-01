import os
from typing import List

import sendgrid
from python_http_client import BadRequestsError
from sendgrid import Email, To, Mail

from parsers import BaseParser


class SendGrid:
    def __init__(self, options: dict, result_parser: BaseParser):
        if not os.environ.get('SENDGRID_API_KEY'):
            raise ValueError('SENDGRID_API_KEY 가 제공되지 않았습니다.')
        self.send_grid = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))

        if not options.get('sender'):
            raise ValueError('option 으로 sender 가 제공되지 않았습니다.')
        if not options.get('recipient'):
            raise ValueError('option 으로 recipient 가 제공되지 않았습니다.')

        self.result_parser = result_parser

        self.from_email = Email(options.get('sender'))
        self.to_email = To(options.get('recipient'))

        self._content = None
        self._title = None

    @property
    def content(self):
        if self._content is None:
            raise ValueError(
                'content 를 호출하기 전 반드시 prepare_data 가 호출되어야합니다.'
            )

        return self._content

    @property
    def title(self):
        if self._title is None:
            raise ValueError(
                'title 을 호출하기 전 반드시 prepare_data 가 호출되어야합니다.'
            )

        return self._title

    def prepare_data(self, results: List[dict], **kwargs):
        self._title = kwargs.get('title')
        if not self._title:
            raise ValueError(
                'send_grid API 를 사용하기 위해서는 prepare_data 에 title 를 제공해야합니다.'
            )

        self._content = self.result_parser.parse(results, title=self._title, sub_title='일간 신규 채용 알리미')

    def send(self):
        mail = Mail(
            from_email=self.from_email,
            to_emails=self.to_email,
            subject=self.title,
            html_content=self.content,
        )

        response = self.send_grid.client.mail.send.post(request_body=mail.get())

        return response
