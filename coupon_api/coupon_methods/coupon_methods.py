from datetime import datetime, timedelta
from typing import List, Optional

from coupon_api.constants import Countries
from coupon_api.coupon_methods.coupon_interface import CouponInterface
from coupon_api.coupon_methods.utils import (
    parse_one_integer_param,
    parse_third_country_param,
    parse_two_integer_params,
)
from coupon_api.data_model.coupon import Coupon
from coupon_api.data_model.coupon_validity import CouponUserValidity
from coupon_api.data_model.service import Service
from coupon_api.data_model.user import User


class AllServiceDiscount(CouponInterface):
    coupon_type_id = 1

    def __init__(self, coupon: Coupon):
        discount_value, expiry_days = parse_two_integer_params(params=coupon.parameters)
        self.discount_percentage = float(discount_value) / 100
        self.expiry_timedelta = timedelta(days=expiry_days)

    def calculate_expiry_date(
        self, user: User, coupon_validity: CouponUserValidity
    ) -> Optional[datetime]:
        expiry_datetime = coupon_validity.expiry_datetime
        if expiry_datetime:
            return expiry_datetime

        return datetime.now() + self.expiry_timedelta

    def activate_coupon_discounts_before_purchase(
        self, user: User, services: List[Service]
    ):
        for service in services:
            service.price = service.price * (1 - self.discount_percentage)

    def activate_coupon_discounts_after_purchase(
        self, user: User, purchased_service: Service
    ):
        # No discount is applied after purchase for this coupon
        pass


class AllServiceDiscountLocalized(AllServiceDiscount):
    coupon_type_id = 2

    def __init__(self, coupon: Coupon):
        super().__init__(coupon)
        self.active_country = parse_third_country_param(params=coupon.parameters)

    def is_useable(
        self,
        user: User,  # pylint: disable=W0613
        coupon_validity: CouponUserValidity,
    ) -> bool:
        return (
            super().is_useable(user=user, coupon_validity=coupon_validity)
            and user.country == Countries.HUNGARY
        )


class NextPurchaseFixDiscount(CouponInterface):
    coupon_type_id = 10

    def __init__(self, coupon: Coupon):
        self.fix_discount_value = parse_one_integer_param(params=coupon.parameters)

    def calculate_expiry_date(
        self, user: User, coupon_validity: CouponUserValidity
    ) -> Optional[datetime]:
        return None

    def activate_coupon_discounts_before_purchase(
        self, user: User, services: List[Service]
    ):
        for service in services:
            service.price -= self.fix_discount_value

    def activate_coupon_discounts_after_purchase(
        self, user: User, purchased_service: Service
    ):
        # No discount is applied after purchase for this coupon
        pass
