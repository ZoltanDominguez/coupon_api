from typing import List

from sqlmodel import JSON, Column, Field, Relationship, SQLModel

from coupon_api.data_model.coupon_validity import CouponUserValidity

CouponParameter = List[str]


class Coupon(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    coupon_type_id: int
    name: str = Field(description="Name of the coupon")
    description: str = Field(
        description="Description of the coupon availability and discount it gives"
    )
    parameters: List[str] = Field(default=None, sa_column=Column(JSON))
    users_of_coupon: List["User"] = Relationship(
        back_populates="coupons_available", link_model=CouponUserValidity
    )

    # Needed for Column(JSON)
    class Config:
        arbitrary_types_allowed = True
