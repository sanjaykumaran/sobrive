import sys
import os

if __package__:
    parentdir = os.path.dirname(__file__)
    rootdir = os.path.dirname(parentdir)
    if rootdir not in sys.path:
        sys.path.append(rootdir)
    if parentdir not in sys.path:
        sys.path.append(parentdir)
    from .base import Base

from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.orm import relationship
from db.userdata import UserData

class User(Base):
    __tablename__ = "users"

    useremail = Column(String(256), nullable=False, primary_key=True)
    emergencyName = Column(String(256), nullable=False)
    emergencyPhone = Column(String(10), nullable=False)
    avgmillis = Column(Integer, nullable=False)
    drivingscore = Column(Integer, nullable=False)
    userdata = relationship("UserData")

    def __init__(self, useremail, emergencyName, emergencyPhone, avgmillis, drivingscore):
        self.useremail = useremail
        self.emergencyName = emergencyName
        self.emergencyPhone = emergencyPhone
        self.avgmillis = avgmillis
        self.drivingscore = drivingscore