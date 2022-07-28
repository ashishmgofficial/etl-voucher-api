# Summary

Data had following issue identified:

1) Empty string values in `total_order` column and was of Object Type
2) Timestamp fields like `last_order_ts` and `timestamp` where of Object type
3) Duplicate records found : 24
4) `Nan` values in `voucher_amount` field

Exploratory Resolution Applied:
1) Empty string values in `total_order` field replaced with `0` and converted to `int` from `object`
2) All timestamp fields converted to `datetime64[ns, UTC]` datetime format 
3) Deduplicated the records and kept the first occurence
4) `voucher_amount` field converted from `object` to `int` and replaced `NaN` with `0`