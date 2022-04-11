import datetime

from great_expectations.core import ExpectationConfiguration
from great_expectations.profile.user_configurable_profiler import UserConfigurableProfiler
import os
from ruamel import yaml
from great_expectations.core.batch import RuntimeBatchRequest
from great_expectations.data_context import BaseDataContext
from great_expectations.data_context.types.base import (
    DataContextConfig,
    FilesystemStoreBackendDefaults,
)

from great_expectations.core.util import get_or_create_spark_application

spark = get_or_create_spark_application(spark_config={'spark.jars.packages':
                                                          'za.co.absa.spline.agent.spark:spark-3.0-spline-agent-bundle_2.12:0.7.4',
                                                      "spark.sql.queryExecutionListeners":
                                                          "za.co.absa.spline.harvester.listener.SplineQueryExecutionListener",
                                                      "spark.spline.producer.url": "http://localhost:8080/producer"})

root_directory = "/home/srinivasan/Documents/DataLineage/ge"

data_context_config = DataContextConfig(
    store_backend_defaults=FilesystemStoreBackendDefaults(
        root_directory=root_directory
    ),
)
context = BaseDataContext(project_config=data_context_config)
uncommitted_directory = os.path.join(root_directory, "uncommitted")

src_df = spark.read \
    .option("header", "true") \
    .option("inferschema", "true") \
    .csv("wikidata.csv")

my_spark_datasource_config = {
    "name": "spark_datasource",
    "class_name": "Datasource",
    "module_name": "great_expectations.datasource",
    "execution_engine": {"class_name": "SparkDFExecutionEngine",
                         "module_name": "great_expectations.execution_engine"},
    "data_connectors": {
        "default_runtime_data_connector_name": {
            "module_name": "great_expectations.datasource.data_connector",
            "class_name": "RuntimeDataConnector",
            "batch_identifiers": [
                "some_key_maybe_pipeline_stage",
                "some_other_key_maybe_run_id",
            ],
        }
    },
}

context.test_yaml_config(yaml.dump(my_spark_datasource_config))

context.add_datasource(**my_spark_datasource_config)
batch_request = RuntimeBatchRequest(
    datasource_name="spark_datasource",
    data_connector_name="default_runtime_data_connector_name",
    data_asset_name="Spark_ge_test",  # This can be anything that identifies this data_asset for you
    batch_identifiers={
        "some_key_maybe_pipeline_stage": "prod",
        "some_other_key_maybe_run_id": f"my_run_name_{datetime.date.today().strftime('%Y%m%d')}",
    },
    runtime_parameters={"batch_data": src_df},  # Your dataframe goes here
)

expectation_suite_name = "test_suite"
context.create_expectation_suite(
    expectation_suite_name=expectation_suite_name, overwrite_existing=True
)
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name=expectation_suite_name,
)
print(validator.head())

profiler = UserConfigurableProfiler(
    profile_dataset=validator,
    excluded_expectations=None,
    not_null_only=False,
    primary_or_compound_key=False,
    semantic_types_dict=None,
    table_expectations_only=False,
    value_set_threshold="MANY",
)
suite = profiler.build_suite()
validator.expect_column_values_to_not_be_null(column="domain_code")
validator.expectation_suite.append_expectation(
    ExpectationConfiguration(expectation_type="expect_column_values_to_be_between",
                             kwargs={'column': 'total_response_size', 'min_value': 1,
                                     'max_value': 12},
                             meta={'reason': 'month should always be in between 1 and 12'}))
validator.save_expectation_suite(discard_failed_expectations=False)

my_checkpoint_name = "test_suite"
checkpoint_config = {"name": my_checkpoint_name, "config_version": 1.0, "class_name": "SimpleCheckpoint",
                     "run_name_template": "%Y%m%d-%H%M%S-my-run-name-template", }
my_checkpoint = context.test_yaml_config(yaml.dump(checkpoint_config))

context.add_checkpoint(**checkpoint_config)

checkpoint_result = context.run_checkpoint(
    checkpoint_name=my_checkpoint_name,
    validations=[
        {
            "batch_request": batch_request,
            "expectation_suite_name": expectation_suite_name,
        }
    ],
)

print(checkpoint_result)
