from sqlalchemy import Column, String, Integer, Date, Boolean
from base import Base

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