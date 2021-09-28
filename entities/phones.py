from sqlalchemy import Column, String, Integer
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))
from base import Base

class Phone(Base):
    __tablename__ = 'phones'

    fiscal_id = Column(String, primary_key=True)
    phone = Column(String, primary_key=True)
    status = Column(String)
    priority = Column(Integer)

    def __init__(self,
                fiscal_id,
                phone,
                status,
                priority
                ):
        self.fiscal_id = fiscal_id
        self.phone = phone
        self.status = status
        self.priority = priority