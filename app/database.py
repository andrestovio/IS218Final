from sqlalchemy import Column, Integer, String, Float
from app.base import Base  # Import Base from base.py

class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True)
    operation = Column(String, nullable=False)
    num1 = Column(Float, nullable=False)
    num2 = Column(Float, nullable=False)
    result = Column(Float, nullable=False)
