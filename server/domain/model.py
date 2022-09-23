from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from database.db import Base, engine
from sqlalchemy.ext.declarative import declared_attr

tables = []

class EntityBase():
    """Entity base model."""
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime)

tables.append('clients')
class Client(EntityBase, Base):
    """Client model."""
    __tablename__ = "clients"

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


tables.append('mechanics')
class Mechanic(EntityBase, Base):
    """Mechanic model."""
    __tablename__ = "mechanics"

    company_logo = Column(String)
    company_name = Column(String)
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
    services = Column(String)
    profile = Column(Integer, ForeignKey("profiles.id"))

tables.append('profiles')
class Profile(EntityBase, Base):
    """profile model."""
    __tablename__ = "profiles"

    name = Column(String)
    description = Column(String)


tables.append('cars')
class Car(EntityBase, Base):
    """Car model."""
    __tablename__ = "cars"

    brand = Column(String)
    model = Column(String)
    version = Column(String)
    year = Column(Integer)
    client = Column(Integer, ForeignKey("clients.id"))


tables.append('services')
class Service(EntityBase, Base):
    """Service model."""
    __tablename__ = "services"

    name = Column(String)
    description = Column(String)

# Create tables
Base.metadata.create_all(engine)
