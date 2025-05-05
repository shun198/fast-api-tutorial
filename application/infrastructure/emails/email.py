from pathlib import Path

from config.env import app_settings
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from jinja2 import Environment, FileSystemLoader, select_autoescape
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


# テンプレート設定
BASE_DIR = Path(__file__).resolve().parent.parent
templates_dir = BASE_DIR / "emails/templates"
jinja_env = Environment(
    loader=FileSystemLoader(str(templates_dir)),
    autoescape=select_autoescape(["html", "xml"]),
)


async def send_email(email: str, template_name: str, subject: str, context: dict):
    template = jinja_env.get_template(template_name)
    html = template.render(context)
    if app_settings.DEBUG:
        message = MessageSchema(
            subject=subject,
            recipients=email,
            body=html,
            subtype=MessageType.html,
        )
        await fm.send_message(message)
    else:
        # sendgrid
        # https://sendgrid.kke.co.jp/docs/Integrate/Code_Examples/v2_Mail/python.html
        # https://github.com/sendgrid/sendgrid-python
        message = Mail(
            subject=subject,
            to_emails=email.model_dump().get("email"),
            from_email="from_email@example.com",
            html_content=html,
        )
        await sg.send(message)
