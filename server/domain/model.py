from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from database.db import Base, engine
from sqlalchemy.ext.declarative import declared_attr

tables = []

class EntityBaseClients():
    """Entity model."""
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime)
    @declared_attr
    def created_by(cls):
        return Column(Integer, ForeignKey("clients.id"))
    modifiet_at = Column(DateTime)
    @declared_attr
    def modifiet_by(cls):
        return Column(Integer, ForeignKey("clients.id"))

tables.append('clients')
class Client(Base):
    """client model."""
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String)
    password = Column(String)
    zip_code = Column(Integer)
    country = Column(String)
    state = Column(String)
    city = Column(String)
    address = Column(String)
    complement = Column(String)
    phone = Column(String)
    identification = Column(String)
    profile = Column(Integer, ForeignKey("profiles.id"))
    created_at = Column(DateTime)

tables.append('profiles')
class Profile(Base):
    """profile model."""
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    created_at = Column(DateTime)

# Create tables
Base.metadata.create_all(engine)
