FROM datamechanics/spark:3.1.3-latest

USER 0

WORKDIR /opt/application
ENV PYSPARK_MAJOR_VERSION=3



COPY . .

RUN pip3 install --upgrade pip setuptools wheel build && pip3 install -e .

