from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Union, List, Optional
from .. import models, utils, schemas,oauth2
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
     prefix="/votes",
     tags=['Votes'] #This is to create group in url/docs
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote, db:Session=Depends(get_db), current_user:int=Depends(oauth2.get_current_user)):

    video=db.query(models.Video).filter(models.Video.id==vote.video_id).first() #First we are checking if that video is there in our db.

    if not video:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"video with id {vote.video_id} does not exist")
    
    vote_query = db.query(models.Vote).filter(models.Vote.video_id==vote.video_id,models.Vote.user_id==current_user.id) #Checking if we already liked the video
    found_vote = vote_query.first()
    
    if(vote.dir==1): 
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail =f"user {current_user.id} already voted on video {vote.video_id}")
        
        
        new_vote= models.Vote(video_id=vote.video_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"Succesfully Added Vote"}
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail ="Vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return{"Succesfully Deleted Vote"}

