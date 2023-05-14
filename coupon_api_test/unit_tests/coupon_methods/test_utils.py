import pytest

from coupon_api.constants import Countries
from coupon_api.coupon_methods.utils import parse_country_param


@pytest.mark.parametrize(
    "country_str, country_enum",
    [
        ("Hungary", Countries.HUNGARY),
        ("hungary", Countries.HUNGARY),
        ("HUNGARY", Countries.HUNGARY),
        ("Austria", Countries.AUSTRIA),
    ],
)
def test_parse_country_param(country_str, country_enum):
    assert parse_country_param(country_str) == country_enum
