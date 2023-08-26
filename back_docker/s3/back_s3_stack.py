from aws_cdk import Stack, CfnOutput
from constructs import Construct
from aws_cdk import (
    aws_s3 as s3,
    RemovalPolicy
)
import os
from dotenv import load_dotenv
from utils.environment import get_name_suffix

load_dotenv()


class S3Bucket(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        name_suffix = get_name_suffix()

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
