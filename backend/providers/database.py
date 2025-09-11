from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
  
SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://sa:federico1@DESKTOP-UQO21FA\SQLEXPRESSFEDE:1433/test_pp2?driver=ODBC+Driver+17+for+SQL+Server"

    #(f'mssql+pymssql://{settings.DB_UID}:{settings.DB_PWD}@{settings.DB_SERVER}:{settings.DB_PORT}/{settings.DB_NAME}')
# engine = create_engine(
#                 SQLALCHEMY_DATABASE_URL,
#                 pool_recycle=3600,
#                 echo_pool=True,
#                 echo=True,
#                 pool_timeout=30,   
#             )
#             SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#             Base = declarative_base()

def iniciar_conexion():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    return engine, SessionLocal, Base


