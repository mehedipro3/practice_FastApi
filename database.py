from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres.wkmaaljvxlkmrtbnvvvp:01312415417++--m@aws-0-ap-northeast-1.pooler.supabase.com:5432/postgres'
## mysql+pymysql://root:password@127.0.0.1:3306/todoapplicationdatabase
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()
