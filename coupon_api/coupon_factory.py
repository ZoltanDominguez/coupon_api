from typing import Dict

from coupon_api.coupon_methods.coupon_interface import CouponInterfaceT
from coupon_api.coupon_methods.coupon_methods import (
    AllServiceDiscount,
    AllServiceDiscountLocalized,
    NextPurchaseFixDiscount,
)
from coupon_api.data_model.coupon import Coupon


class CouponFactory:
    """Registers CouponInterface classes on initialization instantiates"""

    coupon_classes: Dict[int, CouponInterfaceT] = {}

    def __init__(self):
        self.register_coupon_classes()

    def register_coupon_classes(self):
        for coupon in (
            AllServiceDiscount,
            AllServiceDiscountLocalized,
            NextPurchaseFixDiscount,
        ):
            self.coupon_classes[coupon.coupon_type_id] = coupon

    def get_coupon_instance(self, coupon: Coupon) -> CouponInterfaceT:
        coupon_interface_class = self.coupon_classes.get(coupon.coupon_type_id, None)
        if coupon_interface_class is None:
            raise ValueError(
                f"No coupon interface class is registered for coupon: "
                f"{coupon.id=} {coupon.name=}"
            )
        return coupon_interface_class(coupon=coupon)
