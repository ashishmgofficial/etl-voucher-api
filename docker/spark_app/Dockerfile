FROM bitnami/spark:3.3.0

USER 0



ADD --chown=1001:1001 https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.2/hadoop-aws-3.3.2.jar /opt/bitnami/spark/jars/hadoop-aws-3.3.2.jar
ADD --chown=1001:1001 https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.1026/aws-java-sdk-bundle-1.11.1026.jar /opt/bitnami/spark/jars/aws-java-sdk-bundle-1.11.1026.jar
# ENV PYSPARK_MAJOR_VERSION=3
RUN mkdir -p /opt/application && chown -R 1001:root /opt/application && chmod -R 777 /opt/bitnami/spark/jars/
# COPY docker/spark_app/start_spark.sh .

USER 1001