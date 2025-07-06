from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from typing import Optional
from database import Base

# Definindo modelos:
# Um modelo é uma classe que representa uma tabela no banco de dados. Cada atributo representa uma coluna na tabela.

class User(Base):
    __tablename__ = "users" # Define o nome real da tabela no banco.

    id = Column(Integer, primary_key=True, index=True) # primary_key: chave primária, ou seja, identificador único de cada linha da tabela. Só pode haver um único valor por registro nessa coluna.
    name = Column(String, index=True) # index=True: cria um índice sobre a coluna no banco de dados.
    email = Column(String, unique=True, index=True) # unique=True: define que cada registro tenha um valor único.

# Valida os dados recebidos, garantindo que estejam no formato especificado.
class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None