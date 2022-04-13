FROM apache/airflow:2.2.5
USER root
RUN apt-get update \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow
RUN pip install --no-cache-dir --user openlineage-airflow
