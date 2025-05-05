from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType


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


async def send_email(email, html):
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.model_dump().get("email"),
        body=html,
        subtype=MessageType.html,
    )
    await fm.send_message(message)
