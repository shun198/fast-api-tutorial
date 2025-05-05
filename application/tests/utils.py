from config.jwt import hash_password
from infrastructure.database import Base
from models import Users
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

TEST_SQLALCHEMY_DATABASE_URL = "postgresql://test_user:password@db:5432/test_db"

test_engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL, poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    user = Users(
        id=123,
        email="test_user_admin_01@example.com",
        username="test_user_admin_01",
        first_name="user_admin_01",
        last_name="test",
        password=hash_password("test"),
        is_active=True,
        is_admin=True,
        phone_number="08011112222",
    )
    return user
