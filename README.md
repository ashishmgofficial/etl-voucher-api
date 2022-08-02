# VOUCHER CALCULATION API

This application calculates `frequency` and `recency` segmentation of a customer voucher assignment dataset. An API is exposed via which users can retrieve the highest assigned voucher as per the segment and the country the request is made for.

Following are the tech stack used for this project:

1. `Pandas` and `jupyter notebook` : Exploratory data analysis
2. `Pyspark` : Actual transformation framework
3. `Apache Airflow`: Workflow orchestration for the data pipeline.
4. `Postgres DB`: Airflow metastore and `Datawarehouse`
5. `FastAPI`: REST API framework

Following are the logic applied for calculating the `recency` and `frequency` segments:

### Frequency Segment
1. Spark pipeline adds extra columns for `frequency_segment` which segments the data as per the following requirement groups:
    ```
    "0-4" - customers which have done 0-4 orders
    "5-13" - customers which have done 5-13 orders
    "14-37" - customers which have done 14-37 orders 
    ```
2. This data is loaded to data warehouse after cleaning
3. At the datawarehouse, a `view` is created named `customer.frequency_voucher_details_view` which calculates the most used voucher per country per sub variant segment.
4. API retrives the details from the above view and hence is optimized and faster

### Recency Segment
1. Spark pipeline adds extra columns for `recency_segment` which segments the data as per the following requirement groups:
    ```
    "30-60" - 30-60 days since the last order
    "61-90" - 61-90 days since the last order
    "91-120" - 91-120 days since the last order
    "121-180" - 121-180 days since the last order
    "180+" - more than 180 days since the last order 
    ```
2. This data is loaded to data warehouse after cleaning
3. At the datawarehouse, a `view` is created named `customer.recency_voucher_details_view` which calculates the most used voucher per country per sub variant segment.
4. API retrives the details from the above view and hence is optimized and faster

## Project Setup

* Though the entire project is dockerized, spark images has permission issues due to which when executed via spark submit operator in airflow, the jo fails with file not found error. Anyways, I have added the full airflow dag, which is functional when executed via local Airflow installation and master of spark set as local in airflow connections.

Steps:
1. Clone the repository
2. execute following commands at the project root
    ```
    mkdir -p ./airflow/dags ./airflow/logs ./airflow/plugins
    echo -e "AIRFLOW_UID=$(id -u)" > ./airflow/.env
    ```