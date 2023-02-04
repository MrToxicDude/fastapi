from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..db import get_db
from ..func import utils
from ..models.models import User
from ..models.schemas import Register, UpdateUser

router = APIRouter()


@router.post("/users")
def create_user(user: Register, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user =User(**user.dict())

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        cause = e.__cause__
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.args
        )

    






@router.get("/users/{id}")
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id==id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )
    return {"user": user}





@router.put("/users/{id}")
def update_user(id : int, user_data: UpdateUser, db: Session = Depends(get_db)):
    query:Any= db.query(User).filter(User.id==id)

    user = query.first()
    if user is None:
        return {"message":"the user not found"}

    #using exclude_unset for optional parameters for updating
    query.update(user_data.dict(exclude_unset=True),synchronize_session=False)

    db.commit()
    return query.first()



@router.delete("/users/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id==id).first()

    if user is None:
        return{"error": "User not found"}

    db.delete(user)
    db.commit()
    return{"message": "User deleted successfully"}




@router.get("/users")
def all_users( db: Session = Depends(get_db)):
    users = db.query(User).all()

    return {"users": users}

