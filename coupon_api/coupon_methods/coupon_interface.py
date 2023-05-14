from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, TypeVar

from coupon_api.app.errors import CouponAlreadyUsed, CouponExpired
from coupon_api.data_model.coupon import Coupon
from coupon_api.data_model.coupon_validity import CouponUserValidity
from coupon_api.data_model.service import Service
from coupon_api.data_model.user import User

CouponInterfaceT = TypeVar("CouponInterfaceT", bound="CouponInterface")


class CouponInterface(ABC):
    """
    The coupon behavior logic is stored in specific classes implementing this interface.
        coupon_type_id indicates how the coupon is going to behave.

    Each coupon type can have its own parameters and use the configured value in any of
    the interface methods.
    """

    @abstractmethod
    def __init__(self, coupon: Coupon):
        """Initialize the coupon parameters if there is any"""

    @property
    @abstractmethod
    def coupon_type_id(self) -> int:
        """Type of the Coupon"""

    @abstractmethod
    def calculate_expiry_date(
        self, user: User, coupon_validity: CouponUserValidity
    ) -> Optional[datetime]:
        """
        :return: None if never expires
        """

    def is_useable(
        self,
        user: User,  # pylint: disable=W0613
        coupon_validity: CouponUserValidity,
    ) -> bool:
        """
        Checks if coupon is active for the user
        :raises
        """
        now = datetime.now()
        expiry_datetime = coupon_validity.expiry_datetime
        if expiry_datetime and expiry_datetime < now:
            raise CouponExpired
        if coupon_validity.is_used:
            raise CouponAlreadyUsed

        return True

    @abstractmethod
    def activate_coupon_discounts_before_purchase(
        self, user: User, services: List[Service]
    ):
        pass

    @abstractmethod
    def activate_coupon_discounts_after_purchase(
        self, user: User, purchased_service: Service
    ):
        pass
