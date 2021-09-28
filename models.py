from sqlalchemy import Column, String, Integer, Date, Boolean
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
engine = create_engine(f'sqlite:///database.db3')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Customer(Base):
  __tablename__ = 'customers'

  fiscal_id = Column(String, primary_key=True)
  first_name = Column(String)
  last_name = Column(String)
  gender = Column(String)
  birth_date = Column(Date)
  age = Column(Integer)
  age_group = Column(Integer)
  due_date = Column(Date)
  delinquency = Column(Integer)
  due_balance = Column(Integer)
  address = Column(String)
  ocupation = Column(String)
  best_contact_ocupation = Column(Boolean)

  def __init__(self,
        fiscal_id,
        first_name,
        last_name,
        gender,
        birth_date,
        age,
        age_group,
        due_date,
        delinquency,
        due_balance,
        address,
        ocupation,
        best_contact_ocupation
        ):
    self.fiscal_id = fiscal_id
    self.first_name = first_name
    self.last_name = last_name
    self.gender = gender
    self.birth_date = birth_date
    self.age = age
    self.age_group = age_group
    self.due_date = due_date
    self.delinquency = delinquency
    self.due_balance = due_balance
    self.address = address
    self.ocupation = ocupation
    self.best_contact_ocupation = best_contact_ocupation


class Email(Base):
  __tablename__ = 'emails'

  fiscal_id = Column(String, primary_key=True)
  email = Column(String, primary_key=True)
  status = Column(String)
  priority = Column(Integer)

  def __init__(self,fiscal_id,email,status,priority):
    self.fiscal_id = fiscal_id
    self.email = email
    self.status = status
    self.priority = priority


class Phone(Base):
  __tablename__ = 'phones'

  fiscal_id = Column(String, primary_key=True)
  phone = Column(String, primary_key=True)
  status = Column(String)
  priority = Column(Integer)

  def __init__(self,fiscal_id,phone,status,priority):
    self.fiscal_id = fiscal_id
    self.phone = phone
    self.status = status
    self.priority = priority