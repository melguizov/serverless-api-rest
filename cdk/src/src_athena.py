
from aws_cdk import (
    core,
    aws_lambda as lambda_,
    aws_s3 as s3,
    aws_iam as iam,
    aws_glue as glue,
    aws_athena as athena
)

from aws_cdk.aws_apigateway import (
    LambdaIntegration,
    RestApi,
)

from constructs import Construct

class SrcAthena(Stack):
    
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        bucket_name = "Bucket_api_rest_flask"
        bucket = s3.Bucket.from_bucket_name(self, "LambdaStackBucket", bucket_name)

        # Crear un rol de IAM para Glue
        glue_role = iam.Role(self, "GlueServiceRole",
            assumed_by=iam.ServicePrincipal("glue.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSGlueServiceRole")
            ]
        )
        # Otorgar permisos al rol de Glue para acceder al bucket S3
        bucket.grant_read_write(glue_role)

        # Crear una base de datos en Glue
        database = glue.CfnDatabase(self, "Athena_api_rest_flask",
            catalog_id=self.account,
            database_input=glue.CfnDatabase.DatabaseInputProperty(
                name="athena_api_rest_flask"
            )
        )

        # Crear una tabla en Glue que apunte a archivos Avro en S3
        table_hired_employees = glue.CfnTable(self, "hired_employees",
            catalog_id=self.account,
            database_name=database.ref,
            table_input=glue.CfnTable.TableInputProperty(
                name="hired_employees",
                table_type="EXTERNAL_TABLE",
                storage_descriptor=glue.CfnTable.StorageDescriptorProperty(
                    columns=[
                        glue.CfnTable.ColumnProperty(name="id", type="int"),
                        glue.CfnTable.ColumnProperty(name="name", type="string"),
                        glue.CfnTable.ColumnProperty(name="datetime", type="string"),
                        glue.CfnTable.ColumnProperty(name="department_id", type="int"),
                        glue.CfnTable.ColumnProperty(name="job_id", type="int"),

                        # Añade más columnas según tu esquema Avro
                    ],
                    location=f"s3://{bucket.bucket_name}/hired_employees/",
                    input_format="org.apache.hadoop.hive.ql.io.avro.AvroContainerInputFormat",
                    output_format="org.apache.hadoop.hive.ql.io.avro.AvroContainerOutputFormat",
                    serde_info=glue.CfnTable.SerdeInfoProperty(
                        serialization_library="org.apache.hadoop.hive.serde2.avro.AvroSerDe"
                    )
                )
            )
        )

        table_departments = glue.CfnTable(self, "departments",
            catalog_id=self.account,
            database_name=database.ref,
            table_input=glue.CfnTable.TableInputProperty(
                name="departments",
                table_type="EXTERNAL_TABLE",
                storage_descriptor=glue.CfnTable.StorageDescriptorProperty(
                    columns=[
                        glue.CfnTable.ColumnProperty(name="id", type="int"),
                        glue.CfnTable.ColumnProperty(name="department", type="string"),

                        # Añade más columnas según tu esquema Avro
                    ],
                    location=f"s3://{bucket.bucket_name}/departments/",
                    input_format="org.apache.hadoop.hive.ql.io.avro.AvroContainerInputFormat",
                    output_format="org.apache.hadoop.hive.ql.io.avro.AvroContainerOutputFormat",
                    serde_info=glue.CfnTable.SerdeInfoProperty(
                        serialization_library="org.apache.hadoop.hive.serde2.avro.AvroSerDe"
                    )
                )
            )
        )

        table_jobs = glue.CfnTable(self, "jobs",
            catalog_id=self.account,
            database_name=database.ref,
            table_input=glue.CfnTable.TableInputProperty(
                name="jobs",
                table_type="EXTERNAL_TABLE",
                storage_descriptor=glue.CfnTable.StorageDescriptorProperty(
                    columns=[
                        glue.CfnTable.ColumnProperty(name="id", type="int"),
                        glue.CfnTable.ColumnProperty(name="job", type="string"),

                        # Añade más columnas según tu esquema Avro
                    ],
                    location=f"s3://{bucket.bucket_name}/jobs/",
                    input_format="org.apache.hadoop.hive.ql.io.avro.AvroContainerInputFormat",
                    output_format="org.apache.hadoop.hive.ql.io.avro.AvroContainerOutputFormat",
                    serde_info=glue.CfnTable.SerdeInfoProperty(
                        serialization_library="org.apache.hadoop.hive.serde2.avro.AvroSerDe"
                    )
                )
            )
        )