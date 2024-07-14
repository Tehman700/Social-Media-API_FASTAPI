from datetime import time
from fastapi import APIRouter, status, HTTPException
from .. import schemas
import psycopg2
from psycopg2.extras import RealDictCursor
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router_user = APIRouter(
    tags=['All User Information']
)

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='admin', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection was Successful")
        break
    except Exception as error:
        print("Connection failed")
        print(error)
        time.sleep(2)

@router_user.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate):
    hashed = pwd_context.hash(user.password)
    user.password = hashed
    cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s) RETURNING *", (user.email, user.password))
    new_user = cursor.fetchone()
    conn.commit()
    return new_user

@router_user.get("/users/{id}", response_model=schemas.UserOut)
def fetch_user(id: int):
    cursor.execute("SELECT * FROM users WHERE id = %s", (str(id),))
    specific_user = cursor.fetchone()
    if specific_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not Found")
    return specific_user
