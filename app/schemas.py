from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional,Literal



class Token(BaseModel):  #This is for token
    access_token:str
    token_type:str

class TokenData(BaseModel): #This is for tokendata
    id:Optional[str] = None
    email:Optional[EmailStr] = None

#This is used for user schema
class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    created_at: datetime
    
    class Config:
        # orm_mode = True
        from_attributes = True

class UserLogin(BaseModel):
    email:EmailStr
    password:str

#For Videos
class VideoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    video_url: str
    thumbnail_url: Optional[str] = None

class VideoResponse(VideoCreate):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    vote_count: int
    comments_count: int

    class Config:
        from_attributes = True


#For comments

class CommentCreate(BaseModel):
    content: str
    video_id: int

class CommentResponse(CommentCreate):
    id: int
    created_at: datetime
    user_id: int
    user: UserResponse

    class Config:
        from_attributes = True

#Votes
class Vote(BaseModel):
    video_id:int
    dir: Literal[0,1]  #this is for vote like