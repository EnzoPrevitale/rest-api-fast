from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from database import Base

class Dog(Base):
    __tablename__ = "dogs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer, index=True)
    breed = Column(String, index=True)

# Cachorros
class DogCreate(BaseModel):
    name: str
    age: int
    breed: str

class DogResponse(BaseModel):
    id: int
    name: str
    age: int
    breed: str