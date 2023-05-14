from datetime import datetime, timedelta
from typing import Type

import pytest
from fastapi.testclient import TestClient
from httpx import Response
from sqlmodel import Session

from coupon_api.app.errors import (
    CouponAlreadyUsed,
    CouponBaseException,
    CouponDoesNotExist,
    CouponExpired,
)
from coupon_api.data_model.coupon import Coupon
from coupon_api.data_model.coupon_validity import CouponUserValidity

yesterday = datetime.now() - timedelta(days=1)
TEST_DESCRIPTION = "10% Coupon for all services in the next 30 days."
TEST_COUPON_URI = "/users/1/coupons/1251/"


@pytest.fixture(name="valid_coupon")
def coupon_fixture():
    coupon = Coupon(
        id=1251,
        coupon_type_id=1,
        name="name1251",
        description=TEST_DESCRIPTION,
        parameters=["10", "30"],
    )
    yield coupon


def assert_invalid_response(response: Response, error: Type[CouponBaseException]):
    response_json = response.json()
    assert response.status_code == 422, (
        f"HTTP status code was {response.status_code} but it must be 422. "
        f"{response.json()=}"
    )
    assert response_json.get("error_code") == error.api_error.get("error_code")
    assert response_json.get("error_message") == error.api_error.get("error_message")


def assert_valid_coupon(response, coupon: Coupon):
    response_json = response.json()

    assert response.status_code == 200, (
        f"HTTP status code was {response.status_code} but it must be 200"
        f"{response.json()=}"
    )
    assert response_json.get("description") == coupon.description


def test_get_invalid_coupon(
    valid_coupon: Coupon, session: Session, fast_api_client: TestClient
):
    session.add(valid_coupon)
    session.commit()

    response = fast_api_client.get("/users/1/coupons/1252/")
    assert_invalid_response(response, error=CouponDoesNotExist)


def test_get_valid_coupon(
    valid_coupon: Coupon, session: Session, fast_api_client: TestClient
):
    coupon_validity = CouponUserValidity(coupon_id=1251, user_id=1)
    session.add(valid_coupon)
    session.add(coupon_validity)
    session.commit()

    response = fast_api_client.get(TEST_COUPON_URI)
    assert_valid_coupon(response, coupon=valid_coupon)


def test_get_valid_coupon_activated(
    valid_coupon: Coupon, session: Session, fast_api_client: TestClient
):
    coupon_validity = CouponUserValidity(
        coupon_id=1251,
        user_id=1,
        activation_datetime=yesterday,
    )
    session.add(valid_coupon)
    session.add(coupon_validity)
    session.commit()

    response = fast_api_client.get("/users/1/coupons/1251/")
    assert_valid_coupon(response, coupon=valid_coupon)


def test_get_valid_coupon_expired(
    valid_coupon: Coupon, session: Session, fast_api_client: TestClient
):
    coupon_validity = CouponUserValidity(
        coupon_id=1251, user_id=1, expiry_datetime=yesterday
    )
    session.add(valid_coupon)
    session.add(coupon_validity)
    session.commit()

    response = fast_api_client.get("/users/1/coupons/1251/")
    assert_invalid_response(response, error=CouponExpired)


def test_get_valid_coupon_already_used(
    valid_coupon: Coupon, session: Session, fast_api_client: TestClient
):
    coupon_validity = CouponUserValidity(coupon_id=1251, user_id=1, is_used=True)
    session.add(valid_coupon)
    session.add(coupon_validity)
    session.commit()

    response = fast_api_client.get("/users/1/coupons/1251/")
    assert_invalid_response(response, error=CouponAlreadyUsed)
