from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.exc import IntegrityError
from .. import models, utils, schemas
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        # Hash the password
        hashed_password = utils.hash(user.password)
        user.password = hashed_password
        
        # Create new user
        new_user = models.User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
        
    except IntegrityError:
        # This catches duplicate email errors from the database
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )


@router.get("/", response_model=List[schemas.UserResponse])
def get_allusers(db: Session = Depends(get_db)):
    all_users_query = db.query(models.User).all()
    return all_users_query


@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    particular_user = db.query(models.User).filter(models.User.id == id).first()

    if not particular_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {id} does not exist"
        )
    return particular_user