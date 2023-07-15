from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from router import files_api
from router import index

app = FastAPI(title="yunpan")


@app.middleware("http")
async def check_jwt_header(request: Request, call_next):
    # TODO: generate temp password for download and stream
    if (
        request.url.path != "/api/login" and
        request.url.path.startswith("/api") and request.method != "OPTIONS"
    ):
        res = index.check_jwt(
            request.query_params.get("token")
            if request.url.path.startswith("/api/download") or request.url.path.startswith("/api/stream")
            else request.headers.get("jwt")
        )
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

index_file = FileResponse(
    "dist/index.html",
    headers={"Cache-Control": "no-cache"}
)


@app.get("/")
async def read_index():
    return index_file

app.mount("/", StaticFiles(directory="dist"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
