"""Enum objects for the job."""

from enum import Enum
from typing import List


class Domain(Enum):
    """Domain Enum."""

    CUSTOMER = 'customer'

    @classmethod
    def get_registered_domains(cls) -> List[str]:
        """Returns te registered enum values.

        Returns:
            List[str]: Domains
        """
        return [str(domain.value) for domain in cls]
