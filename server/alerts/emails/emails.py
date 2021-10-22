import httpx
import os
from jinja2 import Template
from typing import List
from dotenv import load_dotenv

load_dotenv()


class Service:
    def __init__(self):
        """Initialize email service"""
        self.auth = ("api", os.getenv("MAILGUN_API_KEY"))
        self.base_url = os.getenv("MAILGUN_BASE_URL")

    @staticmethod
    def get_content():
        raise NotImplemented

    def send_mail(self, html: str, subject: str, to: List[str]) -> None:
        """API to send Emails to List[str] of users

        Args:
            html (str): Content
            subject (str): Email Subject
            to (List[str]): List of recipients

        Returns:
            requests.Response: Request response
        """
        data = {
            "from": "Free Watch <aradhyatripathi51@gmail.com>",
            "to": to,
            "subject": subject,
            "html": html,
        }
        if os.getenv("CI"):
            return
        with httpx.Client(auth=self.auth) as client:
            return client.post(url=self.base_url, data=data)


if __name__ == "__main__":
    service = Service()
    print(
        service.send_mail(html="random", subject="tester", to=["at8029@srmist.edu.in"])
    )
