from fastapi import FastAPI, Depends
from . import models,utils,schemas,database,config
from fastapi.middleware.cors import CORSMiddleware
from .routers import video,user,auth,vote,comment


print(config.settings.database_username)

app = FastAPI()

origins=["*"]  #Do this when you want to make api full public and it can be access from anywhere.
#origins=["https://www.google.com"]

#This is for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(video.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(comment.router)

@app.get("/")
def root():
    return {"Welcome to minitube"}