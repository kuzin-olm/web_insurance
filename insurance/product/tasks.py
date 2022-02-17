from django.core.mail import EmailMessage
from celery import shared_task
from django.conf import settings

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


@shared_task
def send_mail_on_response_product(fullname, phone, email, url_product, to):

    text_message = (
        f"<p>Новый отклик на <a href='{url_product}'>продукт</a>.</p>"
        f"<p>От: {fullname}</p>"
        f"<p>т.: {phone}</p>"
        f"<p>email: {email}</p>"
    )

    message = Mail(
        from_email=settings.SENDGRID_SENDER_MAIL,
        to_emails=to,
        subject="Отклик на ваш продукт",
        html_content=text_message,
    )

    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    sg.send(message)
