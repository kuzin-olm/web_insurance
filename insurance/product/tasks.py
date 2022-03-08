from django.core.mail import EmailMessage
from celery import shared_task

from .services import mail


@shared_task
def send_mail_on_response_product(product_response: dict):
    """
    Отправка сообщения о новом отклике на продукт на почту компании.
    """

    subject = "Отклик на ваш продукт"
    to = product_response.get("company_email")
    fullname = product_response.get("full_name")
    phone = product_response.get("phone")
    email = product_response.get("email")
    url_product = product_response.get("url_product")

    text_message = (
        f"<p>Новый отклик на <a href='{url_product}'>продукт</a>.</p>"
        f"<p>От: {fullname}</p>"
        f"<p>т.: {phone}</p>"
        f"<p>email: {email}</p>"
    )

    mail.send(to=to, subject=subject, html_content=text_message)
