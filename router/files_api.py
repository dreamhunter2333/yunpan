import logging
import os
import shutil
import time
import stat

from typing import List

from pydantic import BaseModel
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from fastapi import APIRouter, UploadFile, status, Header

from .config import settings

router = APIRouter()
_logger = logging.getLogger(__name__)


class FileItem(BaseModel):
    name: str
    time: str
    size: str
    isfile: bool


def format_size(size: int, precision: int = 2) -> str:
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    index = 0
    while size >= 1024 and index < len(suffixes) - 1:
        size /= 1024
        index += 1
    return f'{size:.{precision}f} {suffixes[index]}'


@router.get("/list", response_model=List[FileItem], tags=["FileAPi"])
def list_file(path: str = ""):
    out_path = f"{settings.root_path}{os.sep}{path}"
    if not os.path.isdir(out_path):
        _logger.error(f"path {out_path} is not dir")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=f"path {out_path} is not dir"
        )
    _logger.info(f"list {out_path}")

    res = []
    for name in os.listdir(out_path):
        stat_result = os.stat(f"{out_path}{os.sep}{name}")
        if not (stat.S_ISDIR(stat_result.st_mode) or stat.S_ISREG(stat_result.st_mode)):
            continue
        res.append(FileItem(
            name=name,
            time=time.strftime(
                "%Y-%m-%d %H:%M:%S",
                time.gmtime(stat_result.st_mtime)
            ),
            size=format_size(stat_result.st_size),
            isfile=stat.S_ISREG(stat_result.st_mode)
        ))
    return sorted(res, key=lambda item: (1 if item.isfile else 0, item.name))


@router.post("/upload", response_model=bool, tags=["FileAPi"])
def upload(path: str, file: UploadFile):
    out_file_path = f"{settings.root_path}{os.sep}{path}"
    out_path = os.path.dirname(out_file_path)
    if os.path.isfile(out_path):
        _logger.error(f"path {out_path} isfile")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=f"path {out_path} isfile"
        )
    if not os.path.exists(out_path):
        os.makedirs(out_path)
        _logger.info(f"makedirs {out_path}")
    with open(out_file_path, "wb") as f:
        f.write(file.file.read())
    _logger.info(f"uploaded {out_file_path}")
    return True


@router.delete("/delete", response_model=bool, tags=["FileAPi"])
def deleteItem(path: str):
    out_path = f"{settings.root_path}{os.sep}{path}"
    if os.path.isfile(out_path):
        os.remove(out_path)
    else:
        shutil.rmtree(out_path)
    _logger.info(f"delete {out_path}")
    return True


@router.get("/download/{path}", tags=["FileAPi"])
def download_file(path: str, token: str):
    out_file_path = f"{settings.root_path}{os.sep}{path}"
    if not os.path.isfile(out_file_path):
        _logger.error(f"path {out_file_path} is not file")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=f"path {out_file_path} is not file"
        )
    _, filename = os.path.split(out_file_path)
    _logger.info(f"download {out_file_path}")
    return FileResponse(path=out_file_path, filename=filename)


@router.get("/stream/{path}", tags=["FileAPi"])
def stream(path: str, token: str, range: str = Header(None)):
    out_file_path = f"{settings.root_path}{os.sep}{path}"
    file_size = os.stat(out_file_path).st_size
    headers = {
        "accept-ranges": "bytes",
        "content-encoding": "identity",
        "content-length": str(file_size),
        "content-type": "video/webm",
    }
    start = 0
    end = file_size - 1
    status_code = status.HTTP_200_OK

    if range is not None:
        start, end = range.replace("bytes=", "").split("-")
        start = int(start) if start != "" else 0
        end = int(end) if end != "" else file_size - 1
        size = end - start + 1
        headers["content-length"] = str(size)
        headers["content-range"] = f"bytes {start}-{end}/{file_size}"
        status_code = status.HTTP_206_PARTIAL_CONTENT

    def iterfile(chunk_size: int = 10_000):
        with open(out_file_path, "rb") as f:
            f.seek(start)
            while (pos := f.tell()) <= end:
                read_size = min(chunk_size, end + 1 - pos)
                yield f.read(read_size)

    return StreamingResponse(
        iterfile(),
        headers=headers,
        status_code=status_code,
        media_type="multipart/x-mixed-replace;boundary=frame"
    )
