from sqlalchemy.orm import declarative_base, relation, relationship
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime, Time

Base = declarative_base()

"""
any database tables go below, this is the sqlalchemy ORM model
"""

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String, nullable=True)
    salt = Column(String, nullable=True)
    admin = Column(Boolean, nullable=True) # flag to tell if is total admin

class System(Base):
    __tablename__="systems"

    id=Column(Integer, primary_key=True)
    name=Column(String)
    address=Column(String)

class UserPermission(Base):
    __tablename__ = "user_permissions"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    system = Column(Integer, ForeignKey("systems.id"), primary_key=True)


class Camera(Base):
    __tablename__ = "cameras"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    index = Column(Integer)
    system_id = Column(Integer, ForeignKey("systems.id"))
    camera_store_id = Column(Integer, ForeignKey("camera_stores.id"))

class CameraGimbal(Base):
    __tablename__ = "camera_gimbals"

    id = Column(Integer, primary_key=True)
    camera_id = Column(Integer, ForeignKey("cameras.id"))
    x_servo_id = Column(Integer, ForeignKey("servos.id"))
    y_servo_id = Column(Integer, ForeignKey("servos.id"))


class CameraStore(Base):
    __tablename__= "camera_stores"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fs_path = Column(String)
    image_save_time = Column(Time)
    system_id = Column(Integer, ForeignKey("systems.id"))

class Servo(Base):
    __tablename__ = "servos"

    id=Column(Integer, primary_key=True)
    label=Column(String)
    pin=Column(Integer)
    system_id=Column(Integer, ForeignKey("systems.id"))

class Pump(Base):
    __tablename__ = "pumps"

    id = Column(Integer, primary_key=True)
    label = Column(String)
    pin = Column(Integer)
    system_id = Column(Integer, ForeignKey("systems.id"))
    time_to_fill = Column(Integer)

class PumpScheduleEntry(Base):
    __tablename__ = "pump_schedule"

    id = Column(Integer, primary_key=True)
    action = Column(String)
    pump_id = Column(Integer, ForeignKey("pumps.id"))
    #system_id = Column(Integer, ForeignKey("systems.id")) # this could optimize queries but I dont think it will be a realistic use case subquery will slow enough
    days_active = Column(String) #M,T,W,TH,F,S,SU
    times = Column(String) # datetime iso string delimited by commas

    
class DHTSensor(Base):
    __tablename__="dht_sensors"

    id = Column(Integer, primary_key=True)
    label = Column(String)
    pin = Column(Integer)
    dht_type = Column(String)
    system_id = Column(Integer, ForeignKey("systems.id"))