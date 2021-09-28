from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

engine = create_engine(f'sqlite:///{str(BASE_DIR)}/database.db3')

Session = sessionmaker(bind=engine)

Base = declarative_base()

