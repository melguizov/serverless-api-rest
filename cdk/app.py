#!/usr/bin/env python3
import os

import aws_cdk as cdk

from src.src_athena import SrcAthena
from src.src_lambda_api_rest import SrcLambdaApiRest


app = cdk.App()

SrcAthena(app, "SrcAthena")
SrcLambdaApiRest(app, "SrcLambdaApiRest")

app.synth()
