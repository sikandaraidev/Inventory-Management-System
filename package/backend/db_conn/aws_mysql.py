from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker

from package.backend.configuration.config import INVENTORY_DB_URL

# establishing connectivity with AWS MYSQL RDS
engine = create_engine(
    INVENTORY_DB_URL, echo=True, future=True, pool_size=10, max_overflow=20
)


# SQLAlchemy ORM base + session
class Base(DeclarativeBase):
    pass


SessionFactory = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, future=True
)
Session = scoped_session(SessionFactory)


# Sesion for AWS SQLDB
def get_session():
    db_session = Session()
    try:
        yield db_session
    finally:
        db_session.close()
