"""Helper module for the api."""

from typing import List, Optional, Dict, Callable, Any
from enum import Enum
from .exceptions import SegmentVariantNotDefined

FREQUENCY_SEGMENT = {
    '0-4': lambda i: i >= 0 and i <= 4,
    '5-13': lambda i: i >= 5 and i <= 13,
    '14-37': lambda i: i >= 14 and i <= 37,
}
RECENCY_SEGMENT = {
    '0-30': lambda i: i >= 0 and i <= 30,
    '31-60': lambda i: i >= 31 and i <= 60,
    '61-90': lambda i: i >= 61 and i <= 90,
    '91-120': lambda i: i >= 91 and i <= 120,
    '121-180': lambda i: i >= 121 and i <= 180,
    '181+': lambda i: i >= 181,
}


class Segment(Enum):
    """Segments for the voucher api."""

    FREQUENCY = 'frequency_segment'
    RECENCY = 'recency_segment'

    def get_variants(self) -> Dict[str, Callable[[Any], Any]]:
        """Get all the subvarients for the segment."""
        if self.value == 'frequency_segment':
            return FREQUENCY_SEGMENT

        return RECENCY_SEGMENT

    @classmethod
    def get_values(cls) -> List[str]:
        """Returns all the values of the enum as a list."""
        return [e.value for e in cls]


def get_variant_from_segment(identifier: int, segment: Segment) -> Optional[str]:
    """Retrieves the subvariant string as per the segment.

    Args:
        identifier (int): identifier column for calculating the sub variant
        segment (Segment): The parent segment from the payload

    Raises:
        SegmentVariantNotDefined: No segment for the calculated value yet defined.

    Returns:
        Optional[str]: Segment sub variant.
    """
    variants = segment.get_variants()
    for key, condition in variants.items():
        if condition(identifier):
            return key
    raise SegmentVariantNotDefined('Value is out of bounds')
