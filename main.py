from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
app = FastAPI()


# Schema Below:

class Post(BaseModel):
    title: str
    content: str
    published : bool = True # If not provide then no problem otherwise use it
    rating: Optional[int]= None

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 3}, {"title": "favorite foods", "content": "I like Pizza", "id": 2}]



# request Get method url: "/"
# order matters

@app.get("/")
def root(): #root name doesn't mean anything, we can name it accordingly
    return {"message": "Hedfsdg"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/createpostts")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"message" : "successfully created posts"}

@app.post("/createposts")
def create_posts(post : Post):
    print(post)
    # return {"message" : f"title {payload['title']} content: {payload['content']}"}
    return {"data": "post"}

# title str, content str maybe include category, Bool



 



@app.post("/newposts")
def new(post : Post):
    my_dict = post.dict()
    my_dict['id'] = randrange(0,10000000)
    my_posts.append(my_dict)
    return {"data": my_posts}


