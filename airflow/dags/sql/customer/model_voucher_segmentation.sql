
-- Create Frequency Lookup table
create OR REPLACE view customer.frequency_voucher_details_view
as
WITH cte AS (
SELECT 
    country_code , frequency_segment , voucher_amount 
  , ROW_NUMBER() OVER (PARTITION BY country_code ,frequency_segment ORDER BY COUNT(voucher_amount) DESC) rn
FROM customer.voucher_assignment_segmented
GROUP BY
  country_code , frequency_segment , voucher_amount)
SELECT
    country_code , frequency_segment , voucher_amount 
FROM cte WHERE rn = 1;


-- Create Recency Lookup table
create OR REPLACE view customer.recency_voucher_details_view
as
WITH cte AS (
SELECT 
    country_code , recency_segment , voucher_amount 
  , ROW_NUMBER() OVER (PARTITION BY country_code ,recency_segment ORDER BY COUNT(voucher_amount) DESC) rn
FROM customer.voucher_assignment_segmented
GROUP BY
  country_code , recency_segment , voucher_amount)
SELECT
    country_code , recency_segment , voucher_amount 
FROM cte WHERE rn = 1;