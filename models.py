
from sqlalchemy import Column, Integer, String, Text
from database import Base


class UserPlan(Base):
    __tablename__ = "user_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    goal = Column(String(100), nullable=False)
    level = Column(String(30), nullable=False)
    days = Column(Integer, nullable=False)
    plan = Column(Text, nullable=False)
    nutrition_tip = Column(Text, nullable=False)
