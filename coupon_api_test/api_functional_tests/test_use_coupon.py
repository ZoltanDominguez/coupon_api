from sqlmodel import Session
from starlette.testclient import TestClient

from coupon_api.data_model.coupon import Coupon
from coupon_api.data_model.coupon_validity import CouponUserValidity


def test_use_valid_coupon(session: Session, fast_api_client: TestClient):
    coupon_1 = Coupon(
        id=1251,
        coupon_type_id=1,
        name="name1251",
        description="Coupon for all services",
    )
    coupon_validity = CouponUserValidity(coupon_id=1251, user_id=1, is_used=True)
    session.add(coupon_1)
    session.add(coupon_validity)
    session.commit()

    response = fast_api_client.get("/users/1/coupons/1251/")
