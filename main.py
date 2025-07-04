from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Especifica o caminho do banco de dados.
# sqlite é o dialeto do banco de dados. Outros exemplos são mysql, postgresql e etc.
# /// indicam que o caminho é relativo ao diretório atual. //// indicariam que o caminho é absoluto.
# ./test.db é o caminho do banco de dados que será criado ou acessado.
DATABASE_URL = "sqlite:///./test.db"

# Cria a conexão com o banco de dados utilizando a url fornecida no primeiro argumento.
# O segundo argumento, específico do SQLite, é uma opção padrão de segurança do dialeto.
# Ao defini-lo False, permite que a mesma conexão seja compartilhada entre threads (analogia: operários) diferentes, fazendo com que múltiplas requisições possam rodar em paralelo.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# A sessão será utilizada para interagir com o banco de dados, como o cursor da biblioteca sqlite.
# autocommit=False: alterações não são salvas automaticamente.
# autoflush=False: impede que o SQLAlchemy envie alterações pendentes para o banco antes de uma consulta.
#bind=engine: explicita a conexão que será utilizada.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# A base é responsável por gerenciar os modelos e mapeá-los na tabela do banco de dados. Será a superclasse para cada modelo.
Base = declarative_base()

# Definindo modelos:
# Um modelo é uma classe que representa uma tabela no banco de dados. Cada atributo representa uma coluna na tabela.

class User(Base):
    __tablename__ = "users" # Define o nome real da tabela no banco.

    id = Column(Integer, primary_key=True, index=True) # primary_key: chave primária, ou seja, identificador único de cada linha da tabela. Só pode haver um único valor por registro nessa coluna.
    name = Column(String, index=True) # index=True: cria um índice sobre a coluna no banco de dados.
    email = Column(String, unique=True, index=True) # unique=True: define que cada registro tenha um valor único.

# Cria a tabela do banco de dados.
Base.metadata.create_all(bind=engine)

# Gera sessões do banco de dados.
# db = SessionLocal(): cria uma nova sessão do banco de dados utilizando o objeto SessionLocal previamente definido.
# yield: retorna um valor e pausa a função.
# finally: db.close(): fecha a sessão após seu uso, mesmo que ocorra algum erro.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Valida os dados recebidos, garantindo que estejam no formato especificado.
class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str


@app.post("/users/", response_model=UserResponse) # Chama a função ao receber uma requisição POST no endpoint. response_model=User: informa que a função retornará algo no modelo User declarado acima.
def create_user(user: UserCreate, db: Session = Depends(get_db)): 
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name if user.name is not None else db_user.name
    db_user.email = user.email if user.email is not None else db_user.email
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user

# uvicorn main:app --reload