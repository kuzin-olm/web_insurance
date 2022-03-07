from django.conf import settings

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send(to, subject, html_content) -> None:
    """
    Отправка сообщения с помощью сервиса sendgrid.
    """

    message = Mail(
        from_email=settings.SENDGRID_SENDER_MAIL,
        to_emails=to,
        subject=subject,
        html_content=html_content,
    )

    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    sg.send(message)
