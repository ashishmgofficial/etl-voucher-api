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

## Assumptions

1. Test raw data is loaded along with the project to the git repository. Since there is no PII content and being a POC its assumed to be fine.


## Driving Point

This project has been developed with extendability in mind. It is developed with an assumption that the target organization would be having data products or domain centric teams. To cater this requirement, I have implemented code such that it is organized into `Domains` and `Datasets`. Domains are the dta domains like `Customer` in our case and datasets are the different datasets under these domains like `voucher_assignments` in ur case. 

Four CLI arguments are required by the job, 

```bash
❯ voucher_etl --help
usage: voucher_etl [-h] -D {customer} -d DATASET -r RAW_BASEPATH -t PROCESSED_BASEPATH

optional arguments:
  -h, --help            show this help message and exit
  -D {customer}, --domain {customer}
                        Data Domain
  -d DATASET, --dataset DATASET
                        Dataset within domain
  -r RAW_BASEPATH, --raw-basepath RAW_BASEPATH
                        Basepath location of the raw data
  -t PROCESSED_BASEPATH, --processed-basepath PROCESSED_BASEPATH
                        Basepath location of the Processed data
```

The flow of code is controlled by implementing a basic `Factory` pattern for domains and datasets. This makes the code easily extendable and organized.

## CICD

A Basic CI Github Action pipeline with linting, formatting and testing is included with the code at `.github/workflows/` folder


## Project Setup

* You will find the EDA notebooks at `${PROJECT_ROOT}/notebooks` folder with summary README

* Though the entire project is dockerized, spark images has permission issues due to which when executed via spark submit operator in airflow, the job fails with file not found error on Output write. Anyways, I have added the full airflow dag, which is functional when executed via local Airflow installation and master of spark set as local in airflow connections.

Steps:
1. Clone the repository
2. execute following commands at the project root
    ```
    mkdir -p ./airflow/dags ./airflow/logs ./airflow/plugins
    echo -e "AIRFLOW_UID=$(id -u)" > ./airflow/.env
    ```
3. execute following make statements included with the project
    ```
    make compose-prep
    make compose-up
    ```
4. To get up and running, this should take anywhere between 10 to 30 mins depending on the internet speed and workstation.
5. Once everything is up be sure to verify using `docker ps -a` command to see if all services are healthy and are not exited or restarted.
6. If all went well, you should be able to access following services:
    1. `airflow` : `localhost:8080`
    2. `postgres datawarehouse`: `localhost:5432`
    3. You will also get a spark cluster with a master and worker, but due to permission issues, its not usable.
    4. REST API: `localhost:8000`

Following are the default credentials:
1. `airflow`: 
        ```
        username: airflow
        password: airflow
        ```
2. `Datawarehouse`:
        ```
        database: datawarehouse
        username: etl_user
        password: etl_user
        ```
Datawarehouse will not have any data so far, we will load it via our pipeline.

Even though we will not be able to run spark job via airflow docker due to permission issue, I have included a Dockerfile in project root using which we can run the spark job using:
```bash
$ docker build . -t sparkapp:latest
$ docker run -it --mount type=bind,source="$(pwd)"/data,target=/opt/application/data sparkapp:latest driver local:///opt/application/src/etl/main.py --domain customer --dataset voucher --raw-basepath data/raw --processed-basepath data/processed
```

The above command expects the raw dataset to be available at `${PROJECT_ROOT}/data/raw/customer/voucher/` and it generates output at `${PROJECT_ROOT}/data/processed/customer/voucher/`

To run the pipeline now, ( **Complete the Spark job from above before attempting this.**) 
1. Navigate to the airflow UI
2. Toggle the `etl_customer_voucher_assignment` dag on. This should ideally trigger the dag on its own as we have set the schedule to `@once` which will trigger the dag at the earliest.
3. If not triggered, then trigger manually and check the graph view for details.
4. This pipeline will do following things:
    1. Create `customer` schema
    2. Creates the table `customer.voucher_assignment_segmented`
    3. Load the processed csv from previous step of spark run to datawarehouse table `customer.voucher_assignment_segmented`
    4. Generates the `Recency` and `Frequency` views for fast lookup by API

You will find all the `sql` used for these transformation at `sql` folder at `${PROJECT_ROOT}/airflow/`

Once you have the `recency` and `frequency` views successfully loaded, we can try out the `API` started at `localhost:8000/docs`

**REQUEST**

```json
{
  "customer_id": 123,
  "country_code": "Peru",
  "last_order_ts": "2018-05-03 00:00:00",
  "first_order_ts": "2017-05-03 00:00:00",
  "total_orders": 15,
  "segment_name": "recency_segment"
}
```

**RESPONSE**

```json
{
    "voucher_amount": 2640
}
```

**You will find docker files for each service at ${PROJECT_ROOT}/docker folder as well. These are used by docker-compose.yml. The Dockerfile you see at the project root is for packaging up the application and to run the spark job.**

Test cases are available at `tests` folder and following steps should be taken for development activities:

1. `make clean`
2. `make install`
3. `source ./venv/bin/activate`
4. `pytest`