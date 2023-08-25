from aws_cdk import Stack, CfnOutput
from constructs import Construct
from aws_cdk import (
    aws_s3 as s3,
    RemovalPolicy
)
import os
from dotenv import load_dotenv
load_dotenv()


class S3Bucket(Stack):
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


        docker_back_s3bucket = s3.Bucket(
            self,
            "bucketdockerkryvobok"+name_suffix,
            bucket_name="bucketdockerkryvobok"+name_suffix,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        CfnOutput(self, "S3 Bucket ARN", value=docker_back_s3bucket.bucket_arn)
