from typing import Tuple

from coupon_api.app.errors import TooFewCouponParameters
from coupon_api.constants import Countries
from coupon_api.data_model.coupon import CouponParameter


def parse_country_param(country: str) -> Countries:
    country_enum_value = country.lower().capitalize()
    return Countries(country_enum_value)


def check_param_length(params: CouponParameter, length: int):
    print(f"{params=}")
    if not params or len(params) < length:
        raise TooFewCouponParameters


def parse_one_country_param(params: CouponParameter) -> Countries:
    check_param_length(params=params, length=1)
    return parse_country_param(country=params[0])


def parse_third_country_param(params: CouponParameter) -> Countries:
    check_param_length(params=params, length=3)
    return parse_country_param(country=params[2])


def parse_one_integer_param(params: CouponParameter) -> int:
    check_param_length(params=params, length=1)
    return int(params[0])


def parse_two_integer_params(params: CouponParameter) -> Tuple[int, int]:
    check_param_length(params=params, length=2)
    return (
        int(params[0]),
        int(params[1]),
    )
