from fastapi import APIRouter

from coupon_api.data_model.service import Service

service_router = APIRouter(tags=["Service related endpoints"])


@service_router.get(
    path="/users/{user_id}/services/",
    response_model=list[Service],
)
def get_services():
    # get all services
    # get active coupons for the user from CouponUserValidity
    # foreach: activate discount before_purchase
    return {}
