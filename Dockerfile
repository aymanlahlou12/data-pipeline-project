FROM apache/airflow:2.7.2

USER root

RUN apt-get update && apt-get install -y --no-install-recommends default-jre-headless procps && apt-get clean

ENV JAVA_HOME=/usr/lib/jvm/default-java

USER airflow
