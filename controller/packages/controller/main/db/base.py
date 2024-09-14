from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from config import POSTGRES_STRING

engine = create_engine(POSTGRES_STRING)
Session = sessionmaker(bind=engine)
BaseModel = declarative_base()


def init_db():
    BaseModel.metadata.create_all(engine)
