from database import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Users
from sqlalchemy.pool import StaticPool


TEST_SQLALCHEMY_DATABASE_URL = "postgresql://dev_user:password@db:5432/test_db"

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
        # test
        password="$2b$12$7X5m1CKB6CeQRBWfIpoh5ODdLvECJG.YXvPQOwXX.y23hOoxz19P.",
        is_active=True,
        is_admin=True,
        phone_number="08011112222",
    )
    return user
