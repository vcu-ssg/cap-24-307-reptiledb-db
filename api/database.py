import os
import sys
import pymysql
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

# Load environment variables from .env file
load_dotenv()

# Retrieve the database connection details from environment variables
db_user = os.getenv('REPTILEDB_USER')
db_password = os.getenv('REPTILEDB_PASSWORD')
db_host = os.getenv('REPTILEDB_HOST')
db_port = os.getenv('REPTILEDB_PORT')
db_name = os.getenv('REPTILEDB_NAME')
db_sqlite = os.getenv('REPTILEDB_SQLITE')

db_use_db = os.getenv('REPTILEDB_USE_DB')

# Construct the database URL


if db_use_db=="MYSQL":
    db_url = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    engine = create_engine(db_url, connect_args={"connect_timeout": 10})
    db_using_name = f'mysql+pymysql://{db_user}@{db_host}:{db_port}/{db_name}'
elif db_use_db=="SQLITE":
    db_url = f"sqlite:///{db_sqlite}"
    engine = create_engine(db_url)
    db_using_name = db_url
else:
    print(f"No database option selected.\nSet REPTILEDB_USE_DB to MYSQL or SQLITE in .ENV file.")
    sys.exit( 1 )
    


# Create a SQLAlchemy engine

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

def get_db_session():
    """Return a new session."""
    return Session()

if __name__ == "__main__":
    # Test the connection
    try:
        with engine.connect() as connection:
            print(f"Database connection successful! Using {db_using_name}")
    except OperationalError as e:
        if isinstance(e.orig, pymysql.err.OperationalError):
            if e.orig.args[0] in (2003, 2006):
                print(f"Database connection failed: Timeout error. Ensure the server is accessible and not blocking the connection. {e}")
            else:
                print(f"Database connection failed: {e}")
        else:
            print(f"Database connection failed: {e}")
