from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse

from coupon_api.app.coupon_router import coupon_router
from coupon_api.app.errors import (
    CouponBaseException,
    CouponIdUniquenessError,
    GenericIntegrityError,
)
from coupon_api.app.middlewares import LoggerMiddleware
from coupon_api.app.service_router import service_router
from coupon_api.initialization.database import create_db_and_tables
from coupon_api.log import get_logger


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=coupon_router)
app.include_router(router=service_router)
logger = get_logger(name="main")
app.add_middleware(LoggerMiddleware, logger=logger)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.exception_handler(IntegrityError)
async def integrity_exception_handler(_: Request, exc: IntegrityError):
    if "UNIQUE constraint failed: coupon.id" in str(exc):
        raise CouponIdUniquenessError from exc
    raise GenericIntegrityError from exc


@app.exception_handler(CouponBaseException)
async def coupon_exception_handler(_: Request, exc: CouponBaseException):
    logger.error("TooFewCouponParameters in %s", str(exc))
    return JSONResponse(status_code=422, content=exc.api_error)
