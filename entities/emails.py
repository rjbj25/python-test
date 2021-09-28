from sqlalchemy import Column, String, Integer
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))
from base import Base

class Email(Base):
    __tablename__ = 'emails'

    fiscal_id = Column(String, primary_key=True)
    email = Column(String, primary_key=True)
    status = Column(String)
    priority = Column(Integer)

    def __init__(self,
                fiscal_id,
                email,
                status,
                priority
                ):
        self.fiscal_id = fiscal_id
        self.email = email
        self.status = status
        self.priority = priority