import pytest

from database import Base

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import Todos, Users


SQLALCHEMY_DATABASE_URL = "postgresql://test_user:password@db:5432/test_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    user = Users(
        id=123,
        email="test@example.com",
        username="test_user01",
        first_name="user_01",
        last_name="test",
        # test
        password="$2b$12$7X5m1CKB6CeQRBWfIpoh5ODdLvECJG.YXvPQOwXX.y23hOoxz19P.",
        is_active=True,
        is_admin=True,
        phone_number="08011112222",
    )
    return user


@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn to code!",
        description="Need to learn everyday!",
        priority=5,
        complete=False,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()
