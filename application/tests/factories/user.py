from factory import Faker, Sequence
from factory.alchemy import SQLAlchemyModelFactory
from conftest import TestingSessionLocal
import bcrypt
from models import Users


# https://factoryboy.readthedocs.io/en/stable/orms.html#module-factory.alchemy
# https://qiita.com/jk99k/items/387191a380a9a742d8d0
class UsersFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Users
        sqlalchemy_session = TestingSessionLocal

    # ユニーク制約があるのでオートインクリメント
    username = Sequence(lambda n: "テスト利用者{}".format(n))
    password = bcrypt.hashpw(("test").encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    email = Faker("email")
