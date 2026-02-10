from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Union, List, Optional
from .. import models, utils, schemas,oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import func


router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)

# 1️⃣ GET COMMENTS FOR A VIDEO
@router.get("/video/{video_id}", response_model=List[schemas.CommentResponse])
def get_comments_for_video(
    video_id: int,
    db: Session = Depends(get_db)
):
    comments = (
        db.query(models.Comment)
        .filter(models.Comment.video_id == video_id)
        .order_by(models.Comment.created_at.asc())
        
    )
    video_comments = comments.all()
    return video_comments


# 2️⃣ CREATE COMMENT
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CommentResponse)
def create_comment(
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    # Check if video exists
    video = (
        db.query(models.Video)
        .filter(models.Video.id == comment.video_id)
        .first()
    )

    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )

    new_comment = models.Comment(
        content=comment.content,
        video_id=comment.video_id,
        user_id=current_user.id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment

# DELETE COMMENT
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    comment_query = db.query(models.Comment).filter(models.Comment.id == id)
    comment = comment_query.first()

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this comment"
        )

    comment_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
