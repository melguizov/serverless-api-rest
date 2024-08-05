
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

class SrcLambdaApiRest(Stack):
    
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Crear el bucket de S3
        bucket = s3.Bucket(self, "Bucket_api_rest_flask", versioned=True)

        # Crear un rol de IAM para Glue
        glue_role = iam.Role(self, "GlueServiceRole",
            assumed_by=iam.ServicePrincipal("glue.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSGlueServiceRole")
            ]
        )

        # Otorgar permisos al rol de Glue para acceder al bucket S3
        bucket.grant_read_write(glue_role)

        # Crear la función Lambda
        lambda_function = lambda_.Function(
            self, 'Lambda_api_rest_flask',
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler='handler.handler',
            code=lambda_.Code.from_asset('lambda'),
            environment={
                'BUCKET_NAME': bucket.bucket_name
            }
        )

        # Otorgar permisos a la Lambda para acceder al bucket
        bucket.grant_read_write(lambda_function)

        # Crear el API Gateway
        api = RestApi(self, "flask-api", rest_api_name="flask-api")

        root_resource = api.root

        any_method = root_resource.add_method(
            "ANY",
            LambdaIntegration(flask_lambda)
        )