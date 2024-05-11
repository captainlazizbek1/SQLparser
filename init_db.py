from database import Base
# from models import Users
from main import target_db_engine as engine

Base.metadata.create_all(bind=engine)
