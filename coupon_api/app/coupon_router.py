from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session

from coupon_api.app.errors import (
    CouponDoesNotExist,
    CouponNotValidForUser,
    CouponUnusable,
)
from coupon_api.data_model.coupon import Coupon
from coupon_api.data_model.coupon_validity import CouponUserValidity
from coupon_api.data_model.user import User
from coupon_api.initialization.coupon_factory_init import coupon_factory
from coupon_api.initialization.database import get_session

coupon_router = APIRouter(tags=["Coupon related endpoints"])


class CouponValidityResponse(BaseModel):
    is_valid: bool
    coupon: Optional[Coupon]


def get_coupon_user_validity(coupon_id, user_id, session):
    coupon_validity = session.get(CouponUserValidity, (coupon_id, user_id))
    if not coupon_validity:
        raise CouponNotValidForUser
    return coupon_validity


def get_coupon(coupon_id, session):
    coupon = session.get(Coupon, coupon_id)
    if not coupon:
        raise CouponDoesNotExist
    return coupon


@coupon_router.get(
    path="/users/{user_id}/coupons/{coupon_id}",
    response_model=Coupon,
)
def get_coupon_validity(
    user_id: int,
    coupon_id: int,
    session: Session = Depends(get_session),
):
    user = session.get(User, user_id)
    coupon = get_coupon(coupon_id=coupon_id, session=session)
    coupon_validity = get_coupon_user_validity(
        coupon_id=coupon_id, user_id=user_id, session=session
    )

    coupon_executor = coupon_factory.get_coupon_instance(coupon=coupon)
    if not coupon_executor.is_useable(user=user, coupon_validity=coupon_validity):
        raise CouponUnusable

    return coupon


@coupon_router.post(
    path="/users/{user_id}/coupons/{coupon_id}",
    response_model=Coupon,
)
def use_coupon(
    user_id: int,
    coupon_id: int,
    session: Session = Depends(get_session),
):
    validity_response = get_coupon_validity(
        user_id=user_id, coupon_id=coupon_id, session=session
    )
    if not validity_response.get("is_valid"):
        return {"error": "Invalid coupon"}

    user = session.get(User, user_id)
    coupon = session.get(Coupon, coupon_id)
    coupon_validity = session.get(CouponUserValidity, (coupon_id, user_id))

    if coupon_validity.activation_datetime:
        return {"error": "Already activated"}

    coupon_validity.activation_datetime = datetime.now()
    coupon_executor = coupon_factory.get_coupon_instance(coupon=coupon)
    coupon_validity.expiry_datetime = coupon_executor.calculate_expiry_date(
        user=user, coupon_validity=coupon_validity
    )

    session.add(coupon_validity)
    session.commit()
    session.refresh(coupon_validity)
