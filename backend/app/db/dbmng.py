import sys
import os

if __package__:
    parentdir = os.path.dirname(__file__)
    rootdir = os.path.dirname(parentdir)
    if rootdir not in sys.path:
        sys.path.append(rootdir)
    if parentdir not in sys.path:
        sys.path.append(parentdir)
    from .user import User
    from .userdata import UserData
    

def insert_user(session, useremail: bool, emergencyName: str, emergencyPhone: int, avgmillis: int, drivingscore: int):
    x = find_user(session, useremail)    
    user = User(useremail, emergencyName, emergencyPhone, avgmillis, drivingscore)
    
    if x is None:
        session.add(user)
        session.commit()
        return user 
    else: 
        return None
    
def find_user(session, useremail: str):
    x = session.query(User).filter(User.useremail == useremail).first()
    return x

def insert_userdata(session, millies: int, modelresult: bool, datetime: str, useremail: str, sobrietyscore: int):
    userdata = UserData(useremail, millies, modelresult, datetime,sobrietyscore)
    
    session.add(userdata)
    session.commit()

def find_userdata(session, useremail: str):
    x = session.query(UserData).filter(UserData.parentemail == useremail).first()
    return x

def find_all_scores(session, useremail: str):
    x = session.query(UserData).filter(UserData.parentemail == useremail).limit(10).all()
    return x

def find_all_data(session, useremail: str):
    x = session.query(UserData).filter(UserData.parentemail == useremail).all()
    return x

def get_rows_data(session):
    x = session.query(UserData).count()
    return x

def update_user(session, useremail: str, drivingscore: int, avgmillis):
    x = find_user(session, useremail)
    if x is not None:
        x.drivingscore = drivingscore
        x.avgmillis = avgmillis
        session.add(x)
        session.commit()
        return x
    else:
        return None