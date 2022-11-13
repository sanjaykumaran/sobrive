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
    
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey

class UserData(Base):
    __tablename__ = "userdata"
    id = Column(Integer, primary_key=True, autoincrement=True) 
    millies = Column(Integer, nullable=False)
    modelresult = Column(Boolean, nullable=False)
    datetime = Column(String(256), nullable=False)
    sobrietyscore = Column(Integer, nullable=False)
    parentemail = Column(String(256), ForeignKey('users.useremail'), nullable=False)
    
    def __init__(self, parentemail, millies, modelresult, datetime, sobrietyscore):
        self.millies = millies
        self.modelresult = modelresult
        self.datetime = datetime
        self.parentemail = parentemail
        self.sobrietyscore = sobrietyscore