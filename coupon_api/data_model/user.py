from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from coupon_api.data_model.coupon_validity import CouponUserValidity


class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    first_name: str
    last_name: str
    country: str
    wait_list_priority: int = Field(
        default=10_000, description="Lower value means higher priority"
    )
    coupons_available: List["Coupon"] = Relationship(
        back_populates="users_of_coupon", link_model=CouponUserValidity
    )
