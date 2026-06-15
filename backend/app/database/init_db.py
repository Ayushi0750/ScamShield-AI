from app.database.base import Base
from app.database.db import engine

# import all models 
from app.models.analysis import Analysis


def create_tables():
    Base.metadata.create_all(bind=engine)