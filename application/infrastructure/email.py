from config.env import app_settings
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

if app_settings.DEBUG:
    conf = ConnectionConfig(
        MAIL_USERNAME="",
        MAIL_PASSWORD="",
        MAIL_FROM="test@email.com",
        MAIL_PORT=1025,
        MAIL_SERVER="mail",
        MAIL_STARTTLS=False,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=False,
        VALIDATE_CERTS=False,
    )

    fm = FastMail(conf)
else:
    sg = SendGridAPIClient(app_settings.SENDGRID_API_KEY)


async def send_email(email, html):
    if app_settings.DEBUG:
        message = MessageSchema(
            subject="Fastapi-Mail module",
            recipients=email.model_dump().get("email"),
            body=html,
            subtype=MessageType.html,
        )
        await fm.send_message(message)
    else:
        message = Mail(
            subject="Sending with Twilio SendGrid is Fun",
            from_email="from_email@example.com",
            to_emails=email.model_dump().get("email"),
            html_content=html,
        )
        await sg.send(message)


# sendgrid
# https://sendgrid.kke.co.jp/docs/Integrate/Code_Examples/v2_Mail/python.html
# https://github.com/sendgrid/sendgrid-python
