from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

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

# Cria a tabela do banco de dados.
Base.metadata.create_all(bind=engine)