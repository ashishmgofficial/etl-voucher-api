from etl.customer.factory import CustomerDomain
from etl.customer.voucher import VoucherProcessor

domain = CustomerDomain("voucher")


def test_customer_factory():
    processor = domain.get_processor()
    assert isinstance(processor, VoucherProcessor)
