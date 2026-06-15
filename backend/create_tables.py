
from app.database.db import engine
from app.database.base import Base

from app.models.analysis import Analysis
from app.models.recruiter import Recruiter

Base.metadata.create_all(bind=engine)

print("Tables created successfully")