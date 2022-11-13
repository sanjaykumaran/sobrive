from string import ascii_letters, digits
from mangum import Mangum

from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel
from typing import List
from fastapi.responses import JSONResponse
from datetime import datetime

import asyncio



import sys
import os

if __package__:
    parentdir = os.path.dirname(__file__)
    rootdir = os.path.dirname(parentdir)
    if rootdir not in sys.path:
        sys.path.append(rootdir)
    if parentdir not in sys.path:
        sys.path.append(parentdir)

from db.base import engine, SessionLocal, Base
from db.user import User
from db.userdata import UserData
from db import dbmng

from twilio.rest import Client 
import uvicorn
 
account_sid = 'AC9bc01e845ee6faf6fa210a598c1ea151' 
auth_token =  os.environ.get("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token) 

tags_metadata = [
    {
        "name": "Non-Authenticated",
        "description": "API endpoints that do not require authentication.",
    },
    {
        "name": "Authenticated",
        "description": "API endpoints that require authentication.",
    },
]

Base.metadata.create_all(bind=engine)
app = FastAPI(openapi_tags=tags_metadata)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


        
class User_Data(BaseModel):
    millis: int
    modelresult: bool
    datetime: str
    useremail: str
    id: int 

    class Config:
        #modelresult = True if failed model sobriety test
        schema_extra = {
            "example": {
                "millis": 1000,
                "modelresult": True,
                "datetime": "2020-01-01"
            }
        }
        orm_mode = True


class User(BaseModel):
    avgMillis: str
    drivingScore: str
    date: str
    emergencyName: str
    emergencyPhone: int
    email: str
    

    class Config:
        schema_extra = {
            "example": {
                "email": "mxz190024@utdallas.edu",
                "avgMillis": "1000",
                "drivingScore": "78",
                "emergencyName": "John Doe",
                "emergencyPhone": "1234567890",
                "date": "2020-01-01"
            }
        }
        orm_mode = True
responses = {
    400: {
        "content": {
            "application/json": {
                "example": {
                    "status": "400",
                    "message": "Bad request",
                }
            }
        }
    },
    404: {
        "content": {
            "application/json": {
                "example": {
                    "status": "404",
                    "message": "Not found",
                }
            }
        }
    },
    500: {
        "content": {
            "application/json": {
                "example": {
                    "status": "500",
                    "message": "Server Error. Server could be down for maintainance",
                }
            }
        }
    },
}


@app.get(
    "/all",
    tags=["Authenticated"],
    responses={**responses},
)
async def get_User_Info(useremail: str = Query(default=..., description="User email on account"), db: Session = Depends(get_db)):
    
    user_data = dbmng.find_user(db, useremail)
    
    if user_data is None:
        return JSONResponse(status_code=404, content={"message": "User data not found"})
    else:
        return user_data
    

@app.get(
    "/scores",
    tags=["Authenticated"],
    responses={**responses}
)
async def getScores(useremail: str = Query(default=..., description="User email on account"), db: Session = Depends(get_db)):
    
    user = dbmng.find_user(db, useremail)
    scores = dbmng.find_all_scores(db, useremail)
    if user is None:
        return JSONResponse(status_code=404, content={"message": "User not found"})
    else:
        return scores
    
    

@app.post(
    "/adddata",
    tags=["Non-Authenticated"],
    responses={**responses}
)
async def adddata(useremail:str = Query(default= ..., description="user email on account"), millis: int =  Query(default=..., description="Sobriety Time for current test"), sobriety: bool = Query(default=..., description="Updated sobriety result"), db: Session = Depends(get_db)):
    time=datetime.now().strftime("%Y-%m-%d")
    
    score = 0
    
    user = dbmng.find_user(db, useremail)
    length = len(dbmng.find_all_data(db, useremail)) + 1
    prevLen = length - 1
    if(sobriety == False):
        score = 100
    else: 
        user_avg = user.avgmillis
        
        if(length == 0):
            score = 100
            user.drivingscore = user.drivingscore + score
        else:
            user_avg_max = user_avg + user_avg * 0.1
            user_avg_min = user_avg - user_avg * 0.1
            if millis > user_avg_max:
 
                score = (int)(100 - ((millis - user_avg_max) / (user_avg_max * 100)))
                user.drivingscore = (int)((user.drivingscore * prevLen + score)/length) 
                
                user.avgmillis = (int)(user.avgmillis + millis/length)
                message = client.messages.create(  
                              messaging_service_sid='MGb7bf4d30122a64de1d6efffd559bb49a', 
                              body='Hi from Sobrive! We detected drunk driving. Please connect with {x}'.format(x=user.useremail),      
                              to='+1' + str(user.emergencyPhone)
                ) 
                print(message.sid)
            elif millis <= user_avg_min:
                score = (int)(100 - ((user_avg_min - millis) / (user_avg_min * 100)))
                user.drivingscore = (int)((user.drivingscore * prevLen + score)/length)
                
                user.avgmillis = (int)(user.avgmillis + millis/length)
         
    dbmng.insert_userdata(db, millis, sobriety, time, useremail, score)
    dbmng.update_user(db, useremail, user.drivingscore, user.avgmillis)
    
    
    return{"msg": "success"}
    


# handler = Mangum(app=app)
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
