from aws_cdk import Stack, CfnOutput
from constructs import Construct
from aws_cdk import (
    aws_s3 as s3,
    aws_iam as iam,
    RemovalPolicy
)
import os
from dotenv import load_dotenv
load_dotenv()

class FrontMainS3(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        environment = os.environ.get("ENV")

        if environment == "dev":
            name_suffix = "dev"
        elif environment == "main":
            name_suffix = "main"
        elif environment == "test":
            name_suffix = "test"
        else:
            raise ValueError("Unknown environment: {}".format(environment))


        bucket_main = s3.Bucket(
            self,
            "bucket-docker-kryvobok"+name_suffix,
            bucket_name="bucket-docker-kryvobok"+name_suffix,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        CfnOutput(self, "S3 Bucket ARN", value=bucket_main.bucket_arn)
