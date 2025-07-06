from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException

from database import SessionLocal

from users import User, UserCreate, UserResponse, UserUpdate
from dogs import Dog, DogCreate, DogResponse

from typing import List

app = FastAPI()

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

@app.post("/dogs/", response_model=DogResponse)
def create_dog(dog: DogCreate, db: Session = Depends(get_db)):
    db_dog = Dog(name=dog.name, age=dog.age, breed=dog.breed)
    db.add(db_dog)
    db.commit()
    db.refresh(db_dog)
    return db_dog

@app.get("/dogs/", response_model=List[DogResponse])
def read_dogs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    dogs = db.query(Dog).offset(skip).limit(limit).all()
    return dogs

# uvicorn main:app --reload