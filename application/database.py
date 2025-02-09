import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

SQLALCHEMY_DATABASE_URL = os.environ.get("SQLALCHEMY_DATABASE_URL")

# https://docs.sqlalchemy.org/en/20/core/engines.html#engine-configuration
# URLを元にDB用エンジンのオブジェクトを生成
# URLのフォーマットは以下ドキュメントを参考に
# https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-basics
# DBセッションのオブジェクトを生成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase
# Baseクラスを元にモデルを定義する
# SQLAlchemyのバージョン2以降からdeclarative_baseではなく、DeclarativeBaseクラスを使うことが推奨されている
class Base(DeclarativeBase):
    pass
