from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from database.db import Base, engine

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
    permissions = Column(String)


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


tables.append('maintenance_requests')
class Maintenance_Request(EntityBase, Base):
    """Maintenance_Request model."""
    __tablename__ = "maintenance_requests"

    car = Column(Integer, ForeignKey("cars.id"))
    services = Column(String)
    description = Column(String)
    expires_at = Column(DateTime)
    client = Column(Integer, ForeignKey("clients.id"))
    mechanic = Column(Integer, ForeignKey("mechanics.id"))


tables.append('maintenance_responses')
class Maintenance_Response(EntityBase, Base):
    """Maintenance_Response model."""
    __tablename__ = "maintenance_responses"

    status = Column(String)
    request = Column(Integer, ForeignKey("maintenance_requests.id"))
    price = Column(Float)
    message = Column(String)
    proposed_date = Column(DateTime)


tables.append('maintenances')
class Maintenance(EntityBase, Base):
    """Maintenance model."""
    __tablename__ = "maintenances"

    status = Column(String)
    request = Column(Integer, ForeignKey("maintenance_requests.id"))
    response = Column(Integer, ForeignKey("maintenance_responses.id"))


tables.append('mechanical_ratings')
class Mechanical_Rating(EntityBase, Base):
    """Mechanical_Rating model."""
    __tablename__ = "mechanical_ratings"

    rating = Column(Float)
    maintenance = Column(Integer, ForeignKey("maintenances.id"))
    mechanic = Column(Integer, ForeignKey("mechanics.id"))
    comment = Column(String)


tables.append('client_ratings')
class Client_Rating(EntityBase, Base):
    """Client_Rating model."""
    __tablename__ = "client_ratings"

    rating = Column(Float)
    maintenance = Column(Integer, ForeignKey("maintenances.id"))
    client = Column(Integer, ForeignKey("clients.id"))
    comment = Column(String)


# Create tables
Base.metadata.create_all(engine)
