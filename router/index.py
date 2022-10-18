import hmac
import logging
import jwt

from datetime import datetime, timedelta
from json import JSONEncoder

from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi import APIRouter, status

from .config import settings

router = APIRouter()
_logger = logging.getLogger(__name__)


class JwtItem(BaseModel):
    create_at: datetime
    expire_at: datetime


class LoginItem(BaseModel):
    password: str


class DateTimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return JSONEncoder.default(self, obj)


@router.post('/login')
def login_post(login_item: LoginItem):
    if not hmac.compare_digest(settings.password, login_item.password):
        _logger.info(f"login failed with password={login_item.password}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="wrong password"
        )
    jwt_encode = jwt.encode(
        JwtItem(
            create_at=datetime.now(),
            expire_at=datetime.now() + timedelta(days=30)
        ).dict(),
        settings.secret,
        json_encoder=DateTimeEncoder
    )
    return jwt_encode


def check_jwt(jwt_encode: str) -> bool:
    try:
        jwt_item = jwt.decode(
            jwt_encode,
            settings.secret,
            algorithms="HS256",
        )
        jwt_item = JwtItem.parse_obj(jwt_item)
        if jwt_item.expire_at > datetime.now():
            return
    except Exception as e:
        _logger.exception(e)
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content="请重新登录"
    )
