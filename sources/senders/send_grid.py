import os

import sendgrid
from sendgrid import Email, To, Mail


class SendGrid:
    def __init__(self, from_email: str, to_email: str):
        if not os.environ.get('SENDGRID_API_KEY'):
            raise ValueError('SENDGRID_API_KEY 가 제공되지 않았습니다.')
        self.send_grid = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))

        self.from_email = Email(from_email)
        self.to_email = To(to_email)

    def send(self, subject: str, content: str):
        mail = Mail(
            from_email=self.from_email,
            to_emails=self.to_email,
            subject=subject,
            html_content=content,
        )

        response = self.send_grid.client.mail.send.post(request_body=mail.get())

        return response
