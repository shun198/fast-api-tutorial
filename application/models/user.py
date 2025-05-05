from infrastructure.database import Base
from sqlalchemy import Boolean, Column, Integer, String


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    is_admin = Column(Boolean, default=False)
    phone_number = Column(String)
