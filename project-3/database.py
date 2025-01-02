from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

'''
Explicações:
1. Importa a função create_engine do SQLAlchemy. 
Esta função é usada para criar uma conexão com o banco de dados, permitindo que você execute operações de leitura e gravação.

2. Importa a função sessionmaker, que é usada para criar uma "fábrica" de sessões de banco de dados. 
As sessões permitem a interação com o banco (consultas, adição de dados, etc.).

3.  Importa a função declarative_base, que é usada para criar uma classe base a partir da qual 
todos os modelos de tabelas do banco de dados serão derivados.
'''

SQLALCHEMY_DATABASE_URI = 'sqlite:///./todosapp.db'
'''
Define uma string de conexão com o banco de dados. Aqui, está sendo usado o SQLite, e o arquivo do banco de dados será criado no diretório atual com o nome todos.db.
sqlite:/// é o prefixo para usar o SQLite.
./todos.db especifica o caminho relativo do arquivo de banco de dados.
'''

engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={'check_same_thread': False})
'''
Cria o objeto engine, que gerencia a conexão com o banco de dados.
SQLALCHEMY_DATABASE_URI fornece a URI do banco de dados.
connect_args={'check_same_thread': False} é necessário ao usar o SQLite em aplicativos multithread, 
para permitir que diferentes threads usem a mesma conexão.
'''

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
'''
Cria uma fábrica de sessões chamada SessionLocal.
    • autocommit=False desativa o modo de commit automático (você precisará confirmar as transações manualmente).
    • autoflush=False desativa o envio automático de alterações para o banco antes de executar consultas.
    • bind=engine associa a sessão ao engine, que gerencia a conexão com o banco de dados.
'''

Base = declarative_base()
'''
Cria a classe base Base, que será usada para definir modelos de tabelas do banco de dados.
Todos os modelos de tabelas herdarão de Base, o que permite que o SQLAlchemy saiba quais tabelas devem ser criadas ou gerenciadas.
'''
