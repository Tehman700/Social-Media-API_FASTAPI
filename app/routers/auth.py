from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, schemas, models, token_creation
from passlib.context import CryptContext

pwd_context =CryptContext(schemes=["bcrypt"], deprecated = "auto")


router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not pwd_context.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Password")

    access_token = token_creation.create_token(data={"user_id": str(user.id)})  # Ensure user_id is a string
    return {"token": access_token, "token_type": "bearer"}
