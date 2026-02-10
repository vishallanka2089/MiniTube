"""First we use login method in auth.py. That checks username and password and then calls create access token method. It creates a token and sends it back to the user in the response. Now we can add the get current user in other http methods like creating, deleting, fetching posts etc. This checks that the user is logged in. the get current user method then calls the verify access token method to check that the signature and all details are correct. If it matches then user can proceed. The token is generally stored in local storage or similar so user can use all functionalities with just one password and access JWT token.

1. User logs in with email/password
   ↓
2. Server validates and creates JWT token
   ↓  
3. Server returns: {"access_token": "xyz", "token_type": "bearer"}
   ↓
4. Client stores token
   ↓
5. For protected routes, client sends: Authorization: Bearer xyz
   ↓
6. Server validates token and allows/denies access """


from jose import JWTError, jwt #pip install python-jose[cryptography]
from datetime import datetime,timedelta,timezone
from . import schemas,database,models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings




oauth2scheme = OAuth2PasswordBearer(tokenUrl='login') #login is the endpoint in auth file.

#Secret Key
#Algorithm (HS256)
#Expiration time of token

SECRET_KEY = settings.secret_key #they gave same in video and documentation
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data:dict): #data is the info that we want to put in the token that we send back to the client in response.
    to_encode = data.copy() #we don't want to change original data payload so we made copy.


    expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode , SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM]) #This will store all payload data

        id:str = payload.get("user_id")
        email:str = payload.get("user_email")

        if id is None:
            raise credentials_exception
        token_data=schemas.TokenData(id=str(id),email=email) #id is int so we need to convert to str because in schemas we gave id as str. This is out jwt token data. Check this data in jwt.io website
        #token_data = schemas.TokenData(id=str(id))
        #print(token_data) #tHIS WILL PRINT  ID ='' email =''
        
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token:str = Depends(oauth2scheme),db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate crednetials",headers={"WWW-Authenticate":"Bearer"})
    #Here we are trying to verify and get back the entire token body to send to other HTTP Methods.
    token_data = verify_access_token(token,credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()

    if user is None:
        raise credentials_exception
    return user
