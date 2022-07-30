from enum import Enum
from typing import List


class Domain(Enum):
    CUSTOMER = 'customer'

    @classmethod
    def get_registered_domains(cls) -> List[str]:
        return [str(domain.value) for domain in cls]
