--Create table voucher_assignment_segmented in customer schema
CREATE TABLE IF NOT EXISTS customer.voucher_assignment_segmented
(
    "timestamp" TIMESTAMP,
    "country_code" VARCHAR,
    "last_order_ts" TIMESTAMP,
    "first_order_ts" TIMESTAMP,
    "total_orders" INT,
    "voucher_amount" INT,
    "frequency_segment" VARCHAR,
    "recency_segment" VARCHAR
);



--Load preprocessed data to data warehouse 
TRUNCATE table customer.voucher_assignment_segmented;
COPY customer.voucher_assignment_segmented FROM PROGRAM 'cat /var/lib/postgresql/processed/customer/voucher/*.csv' csv header ;