# import re
from pydantic import BaseModel

# EmailStr, field_validator
# from email_validator import validate_email, EmailNotValidError


class CreateUserRequest(BaseModel):
    username: str
    # To use this type, you need to install the optional [`email-validator`](https://github.com/JoshData/python-email-validator) package
    email: str
    first_name: str
    last_name: str
    password: str
    is_admin: bool
    phone_number: str

    # # https://stackoverflow.com/questions/76972389/fastapi-pydantic-how-to-validate-email
    # @field_validator("email")
    # @classmethod
    # def validate_custom_email(cls, value):
    #     try:
    #         allowed_domains = {"gmail.com", "test.com"}
    #         # Check that the email address is valid. Turn on check_deliverability
    #         # for first-time validations like on account creation pages (but not
    #         # login pages).
    #         emailinfo = validate_email(value, check_deliverability=True)
    #         email = emailinfo.normalized
    #         if emailinfo.ascii_domain not in allowed_domains:
    #             raise ValueError(
    #                 f"Only emails from {', '.join(allowed_domains)} are allowed"
    #             )
    #         # After this point, use only the normalized form of the email address,
    #         # especially before going to a database query.
    #         """The normalized email address, which should always be used in preference to the original address.
    #         The normalized address converts an IDNA ASCII domain name to Unicode, if possible, and performs
    #         Unicode normalization on the local part and on the domain (if originally Unicode). It is the
    #         concatenation of the local_part and domain attributes, separated by an @-sign."""
    #         if not email.isascii():
    #             raise ValueError("Invalid email format")
    #         return email
    #     except EmailNotValidError:
    #         raise ValueError("Invalid email format")

    # @field_validator("password")
    # @classmethod
    # def validate_password(cls, value: str) -> str:
    #     password_regex = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,64}$")

    #     if not password_regex.match(value):
    #         raise ValueError(
    #             "Password must be 8-64 characters long, include at least one uppercase letter, one lowercase letter, and one number."
    #         )

    #     return value


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class CurrentUser(BaseModel):
    username: str
    id: int
