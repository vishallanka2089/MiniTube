from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Union, List, Optional
from .. import models, utils, schemas,oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import func

router  = APIRouter(
    prefix="/videos",
    tags=["Videos"] #This is to create group in url/docs
)

#GETTING ALL VIDEOS
@router.get("/",response_model=List[schemas.VideoResponse])
def fetch_videos(db:Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    print("This is current user email: ",current_user.email)
    print("This is current user id: ",current_user.id)

    video_fetch_query = (db.query(
            models.Video,
            func.count(func.distinct(models.Vote.user_id)).label("vote_count"),
            func.count(func.distinct(models.Comment.id)).label("comments_count"),
        )
        .outerjoin(models.Vote, models.Vote.video_id == models.Video.id)
        .outerjoin(models.Comment, models.Comment.video_id == models.Video.id)
        .group_by(models.Video.id)
    )

    print("This is Video_fetch_query:", video_fetch_query)

    all_videos = video_fetch_query.all()
    print("This is result of all_Videos: ",all_videos)

    result = []
    for video, vote_count, comments_count in all_videos:
        result.append({
            **video.__dict__,
            "owner": video.owner,
            "vote_count": vote_count,
            "comments_count": comments_count
        })
    print("This is result of all videos fetch : ", result)
    return result


#Getting videos based on particular user

@router.get("/user/{user_id}", response_model=List[schemas.VideoResponse])
def fetch_videos_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    video_fetch_query = (
        db.query(
            models.Video,
            func.count(func.distinct(models.Vote.user_id)).label("vote_count"),
            func.count(func.distinct(models.Comment.id)).label("comments_count"),
        )
        .outerjoin(models.Vote, models.Vote.video_id == models.Video.id)
        .outerjoin(models.Comment, models.Comment.video_id == models.Video.id)
        .filter(models.Video.owner_id == user_id)
        .group_by(models.Video.id)
    )

    print("This is Video_fetch_query for one user:", video_fetch_query)

    videos = video_fetch_query.all()

    result = []
    for video, vote_count, comments_count in videos:
        result.append({
            **video.__dict__,
            "owner": video.owner,
            "vote_count": vote_count,
            "comments_count": comments_count
        })
    print("This is result of all videos fetch based on one user : ", result)
    return result


# CREATE / UPLOAD VIDEO
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.VideoResponse)
def create_video(
    video: schemas.VideoCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    new_video = models.Video(
        owner_id=current_user.id,
        **video.model_dump()
    )

    db.add(new_video)
    db.commit()
    db.refresh(new_video)

    return {
    **new_video.__dict__,
    "owner": current_user,
    "vote_count": 0,
    "comments_count": 0
}


# UPDATE VIDEO
@router.put("/{id}", response_model=schemas.VideoResponse)
def update_video(
    id: int,
    updated_video: schemas.VideoCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    video_query = db.query(models.Video).filter(models.Video.id == id)
    video = video_query.first()

    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )

    if video.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this video"
        )

    video_query.update(updated_video.model_dump(), synchronize_session=False)
    db.commit()

    updated = video_query.first()

    return updated


# DELETE VIDEO
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_video(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    video_query = db.query(models.Video).filter(models.Video.id == id)
    video = video_query.first()

    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )

    if video.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this video"
        )

    video_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
