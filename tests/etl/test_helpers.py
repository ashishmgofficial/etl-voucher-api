from etl.helpers import replace_missing


# def test_get_spark():
#     session = get_spark()
#     assert isinstance(session, SparkSession) == True


def test_replace_missing(spark_session):
    data = [("", None, 123), ("norway", "europe", 123), ("india", "asia", 100)]
    df = spark_session.createDataFrame(data, ["country", "region", "code"])

    test_df = replace_missing(df, ["region"], "NA")

    assert test_df.filter("region='NA'").count() == 1
