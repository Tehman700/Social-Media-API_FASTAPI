from fastapi import FastAPI
from .routers import post, user, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)


app.include_router(post.router_post)
app.include_router(user.router_user)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}
