from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas,models,utils, oauth2

router= APIRouter(tags=['Authentication'])

@router.post('/login',response_model=schemas.Token)
#def login(user_credentials: schemas.UserLogin, db:Session = Depends(database.get_db)):
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db)):  #We used OAuth2PasswordRequestForm which is built in functionality of fastAPI.
    
    #user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first() #Here we replaced to username because OAuth2PasswordRequestForm only gives back the fields username and password. So even if we have email or anything we will only get it back as username. Also when using this the input values must be given in form-data tab in postman and not in raw.
    #print(user.id, user.email,user.password,user.created_at)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password,user.password): #Incorrect Password
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    access_token = oauth2.create_access_token(data={"user_id":user.id,"user_email":user.email}) #we are putting our user id in jwt token
    #access_token = oauth2.create_access_token(data={"user_id":user.id})
    return {"access_token":access_token, "token_type":"bearer"}
    

    
