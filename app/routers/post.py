from fastapi import APIRouter, Response, status, HTTPException, Depends
from typing import List
from .. import schemas, token_creation
import psycopg2
from psycopg2.extras import RealDictCursor
import time

router_post = APIRouter(
    tags=['All Post Information']
)

# I have made post and users portion in seperate files to ensure more easy reading

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


# showing all the posts

@router_post.get("/posts", response_model=List[schemas.Post])
def get_posts(Limit: int =10):
    cursor.execute(f"SELECT * FROM posts LIMIT {Limit}")
    sql_posts = cursor.fetchall()
    return sql_posts

# creating new posts using raw sql queries and making changes to postgresql admin

@router_post.post("/newposts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def new(post: schemas.PostCreate, get_current_user: int = Depends(token_creation.get_current_user)):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()

    # my_dict = post.dict()
    # my_dict['id'] = randrange(0,10000000)
    # my_posts.append(my_dict)
    return new_post

# Fetching latest posts from the list

@router_post.get("/posts/latest")
def latest_post():
    cursor.execute("SELECT * FROM posts ORDER BY id DESC LIMIT 1")
    post = cursor.fetchone()
    return post


#  fetiching post wrt to given id, if id not in the database, then show http error code

@router_post.get("/posts/{id}", response_model=schemas.Post)
def get_single_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    specific_post = cursor.fetchone()
    if specific_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not Found")
    return specific_post

# same mechanism for detelt post

@router_post.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, get_current_user: int = Depends(token_creation.get_current_user)):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    deleted_post = cursor.fetchone()
    # 204 doesnot ahows anything

    # my_posts.pop(index)
    conn.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found to be deleted")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# updating the post so we can change, wrt to id
@router_post.put("/posts/{id}", response_model=schemas.Post)
def updating(id: int, post: schemas.PostCreate, get_current_user: int = Depends(token_creation.get_current_user)):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, str(id)))
    updated = cursor.fetchone()
    conn.commit()
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found to be updated")
    return updated
