from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import Base  # Import the Base and AdminUser from your models.py

engine = create_engine(f"sqlite:///reptile.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

