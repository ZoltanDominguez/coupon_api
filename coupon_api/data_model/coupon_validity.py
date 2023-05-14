from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class CouponUserValidity(SQLModel, table=True):
    coupon_id: Optional[int] = Field(
        default=None, foreign_key="coupon.id", primary_key=True
    )
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    activation_datetime: Optional[datetime]
    expiry_datetime: Optional[datetime]
    is_used: Optional[bool]
