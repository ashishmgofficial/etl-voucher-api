"""Main APP entrypoint."""

from typing import Any
from fastapi import FastAPI, Depends
from .db import get_connection
from .schemas import CustomerRequestObject
from .helper import Segment, get_variant_from_segment
from datetime import datetime
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()


def find_segment_variant(payload: CustomerRequestObject) -> str:
    """Determine the segment sub variant for the given segment.

    Args:
        payload (CustomerRequestObject): The api json payload object

    Raises:
        ValueError: If not a valid segment.
        ValueError: if not segment is provided.

    Returns:
        str: Segment variant string
    """
    variant = ""
    if not payload.segment_name:
        raise ValueError("Pleae provide a valid segment category")

    if payload.segment_name not in Segment.get_values():
        raise ValueError("Invalid Segment provided")

    if payload.segment_name == Segment.RECENCY:
        last_order_ts = datetime.strptime(payload.last_order_ts, "%Y-%m-%dT%H:%M:%S.%fZ")
        current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        current_timestamp = datetime.strptime(current_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        total_days_since_last_order = (current_timestamp - last_order_ts).days
        variant = get_variant_from_segment(total_days_since_last_order, Segment.RECENCY)

    if payload.segment_name == Segment.FREQUENCY:
        total_orders = payload.total_orders
        variant = get_variant_from_segment(total_orders, Segment.FREQUENCY)

    return variant


def get_voucher_amount(
    conn: Any, segment_name: str, segment_value: str, country_code: str, schema: str
) -> int:
    """Retrieves the voucher amount from the db views.

    Args:
        conn (Any): DB Connection handle
        segment_name (str): The parent segment name from API Payload
        segment_value (str): The sub segment variant
        country_code (str): Country code requested
        schema (str): the database schema for the data views

    Raises:
        e: Generic exception.

    Returns:
        int: The most used voucher amount for the variant in a given country
    """
    try:

        table_name = "recency_voucher_details_view"
        if segment_name == "frequency_segment":
            table_name = "frequency_voucher_details_view"
        cursor = conn.cursor()

        query = f'''
            select
                voucher_amount
            from {schema}.{table_name}
            where lower(country_code) = '{country_code.lower()}'
            and {segment_name} = '{segment_value}'
        '''

        cursor.execute(query)

        amount = cursor.fetchone()

    except Exception as e:
        raise e

    finally:

        cursor.close()
        conn.close()

    return amount[0] if amount else None


@app.get('/health')
def health():
    """Health check endpoint."""
    return 'OK'


@app.post("/get-segment-voucher")
async def get_segment_vouchers(payload: CustomerRequestObject, conn=Depends(get_connection)):
    """API to get the most provided voucher values for a segment in a country.

    Args:
        payload (CustomerRequestObject): Input Payload object.
        conn (_type_, optional):  Defaults to Depends(get_connection).
    """

    try:
        segment_variant = find_segment_variant(payload)
        voucher_amount = get_voucher_amount(
            conn, payload.segment_name, segment_variant, payload.country_code, "customer"
        )

        if voucher_amount is None:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

        return {'voucher_amount': f'{voucher_amount}'}

    except BaseException as e:
        detail = f"Unexpected error occured: {e}"
        raise HTTPException(status_code=500, detail=detail)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=9099)
