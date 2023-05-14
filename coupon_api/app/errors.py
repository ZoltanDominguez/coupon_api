from typing import TypedDict


class Error(TypedDict):
    error_code: int
    error_message: str


class CouponBaseException(Exception):
    api_error: Error


# -------------------- Generic errors
class GenericError(CouponBaseException):
    api_error = Error(error_code=1000, error_message="Unexpected exception")


# -------------------- Database errors
class GenericIntegrityError(CouponBaseException):
    api_error = Error(error_code=2000, error_message="Integrity error")


class CouponIdUniquenessError(CouponBaseException):
    api_error = Error(
        error_code=2010, error_message="UNIQUE constraint failed: coupon.id"
    )


# -------------------- Validity errors
class CouponDoesNotExist(CouponBaseException):
    api_error = Error(error_code=3000, error_message="Coupon does not exist")


class CouponNotValidForUser(CouponBaseException):
    api_error = Error(
        error_code=3001, error_message="Coupon is not created for this user"
    )


class CouponExpired(CouponBaseException):
    api_error = Error(error_code=3010, error_message="Coupon already expired")


class CouponAlreadyUsed(CouponBaseException):
    api_error = Error(error_code=3011, error_message="Coupon already used")


class CouponUnusable(CouponBaseException):
    api_error = Error(error_code=3012, error_message="Coupon cannot be used")


# -------------------- Coupon misconfiguration errors
class TooFewCouponParameters(CouponBaseException):
    api_error = Error(
        error_code=4000, error_message="This coupon type needs more parameters"
    )
