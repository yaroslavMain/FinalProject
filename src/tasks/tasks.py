from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from src.celery import celery, SETTINGS

# iaroslavtulyakov@yandex.ru
# xsslhoyveqfkoott
@celery.task
def send_message(payload: str, to: str):
    msg = MIMEMultipart()
    msg['From'] = SETTINGS.SMTP_USER
    msg['To'] = to
    msg['Subject'] = 'FastApi Test'

    msg.attach(MIMEText(f'There is one stage of registration left. Follow the link {payload} and you will finish registering'))

    server = smtplib.SMTP(SETTINGS.SMTP_HOST, SETTINGS.SMTP_PORT)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(SETTINGS.SMTP_USER, SETTINGS.SMTP_PASSWORD.get_secret_value())
    server.sendmail(
        SETTINGS.SMTP_USER,
        to,
        msg.as_string()
    )
    server.quit()
