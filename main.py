from fastapi import FastAPI
from api.question_answering import router
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

origins = ["http://localhost:5173", os.getenv("WEB_URL")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
