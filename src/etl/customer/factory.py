"""The factory class for the customer domain."""

from dataclasses import dataclass
from etl.customer.voucher import VoucherProcessor


@dataclass
class CustomerDomain:
    """Customer Domain Factory class."""

    dataset: str

    def get_processor(self):
        """Generate the dataset processor under the customer domain."""
        if self.dataset.lower() == 'voucher':
            return VoucherProcessor()
