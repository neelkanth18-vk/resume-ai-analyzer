from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from core.config import settings
import sys
from sqlalchemy.engine.url import make_url

url = make_url(settings.DATABASE_URL)

print("Driver:", url.drivername)
print("Host:", url.host)
print("Port:", url.port)
print("Database:", url.database)

engine = create_engine(settings.DATABASE_URL)

print("DATABASE_URL START")
print(repr(settings.DATABASE_URL))
print("DATABASE_URL END")
sys.stdout.flush()

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()