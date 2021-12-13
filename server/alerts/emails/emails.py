import httpx
import os
from typing import List
from dotenv import load_dotenv
import free_watch

load_dotenv()


class Service:
    def __init__(self):
        """Initialize email service"""
        self.auth = ("api", os.getenv("MAILGUN_API_KEY"))
        self.base_url = os.getenv("MAILGUN_BASE_URL")

    @staticmethod
    def get_content():
        raise NotImplementedError

    def send_mail(self, html: str, subject: str, to: List[str]) -> None:
        """API to send Emails to List[str] of users

        Args:
            html (str): Content
            subject (str): Email Subject
            to (List[str]): List of recipients

        Returns:
            httpx.client.post
        """
        data = {
            "from": os.getenv("email_addr"),
            "to": to,
            "subject": subject,
            "html": html,
        }
        if not free_watch.flags.send_email:
            return
        with httpx.Client(http2=True, auth=self.auth) as client:
            return client.post(url=self.base_url, data=data)
