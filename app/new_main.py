from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models,schemas
from typing import List


app = FastAPI()







while True:

    try:
        # conn = con.connect(host, database, user, password)
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user='postgres', password = 'admin', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection was Successfull")
        break

    except Exception as error:
        print("Connection failed")
        print(error)
        time.sleep(2)


my_posts = []

def find_index(id):
    for i , p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/posts", response_model=List[schemas.Post])
def get_posts():

    # SQL SYSTEM    

    cursor.execute(""" SELECT * FROM posts """)
    sql_posts=cursor.fetchall()
    # print(sql_posts)
    return sql_posts







@app.post("/newposts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def new(post : schemas.PostCreate):

    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))



    new_post = cursor.fetchone()
    conn.commit()





    # my_dict = post.dict()
    # my_dict['id'] = randrange(0,10000000)
    # my_posts.append(my_dict)
    return new_post


@app.get("/posts/latest")
def latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}





@app.get("/posts/{id}", response_model=schemas.Post)   # To see specific post with ID , known as path parameter
def get_single_post(id: int, response : Response):


    cursor.execute(""" SELECT * FROM posts WHERE id = %s """,(str(id),))
    specific_post =cursor.fetchone()
    
    if specific_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not Found")


    return specific_post




 


# To Delete a Post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # find the index in the array that has required ID
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()


    # index = find_index(id)
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post not found to be deleted")
    # 204 doesnot ahows anything

    # my_posts.pop(index)

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}", response_model=schemas.Post)
def updating(id: int, post: schemas.PostCreate):

    cursor.execute(""" UPDATE posts SET title = %s, content
                   = %s, published = %s WHERE id= %s RETURNING *""", (post.title, post.content, post.published, str(id),))

    # index = find_index(id)

    updated = cursor.fetchone()
    conn.commit()
    if updated == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post not found to be updated")


    # post_dict = post.dict()
    # post_dict["id"] = id
    # my_posts[index] = post_dict
    return updated