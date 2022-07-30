from dataclasses import dataclass
from etl.customer.voucher import VoucherProcessor


@dataclass
class CustomerDomain:
    dataset: str

    def get_processor(self):
        if self.dataset.lower() == 'voucher':
            return VoucherProcessor()
