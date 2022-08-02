"""API response schema class."""

from pydantic import BaseModel


class CustomerRequestObject(BaseModel):
    """API Request payload schema object."""

    customer_id: int
    country_code: str
    last_order_ts: str
    first_order_ts: str
    total_orders: int
    segment_name: str
