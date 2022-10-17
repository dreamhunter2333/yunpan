from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router import files_api

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(files_api.router, prefix="")
