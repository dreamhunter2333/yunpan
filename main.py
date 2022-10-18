from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from router import files_api
from router import index

app = FastAPI()


@app.middleware("http")
async def check_jwt_header(request: Request, call_next):
    # TODO: generate temp password for download and stream
    if (
        request.url.path not in ("/api/login", "/api/download", "/api/stream") and
        request.url.path.startswith("/api") and request.method != "OPTIONS"
    ):
        res = index.check_jwt(request.headers.get("jwt"))
        if res:
            return res
    response = await call_next(request)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(files_api.router, prefix="/api")
app.include_router(index.router, prefix="/api")
