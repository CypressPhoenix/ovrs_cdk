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
        # Настройка CORS
        cors_rule = s3.CorsRule(
            allowed_methods=[s3.HttpMethods.GET, s3.HttpMethods.PUT, s3.HttpMethods.POST, s3.HttpMethods.DELETE],  # Разрешенные HTTP методы
            allowed_origins=["*"],  # Разрешенные домены (в данном случае, все)
            allowed_headers=["*"],  # Разрешенные заголовки
        )

        docker_back_s3bucket = s3.Bucket(
            self,
            "bucketdockerkryvobok"+name_suffix,
            bucket_name="bucketdockerkryvobok"+name_suffix,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            cors=[cors_rule],  # Добавляем CORS правило здесь
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        CfnOutput(self, "S3 Bucket ARN", value=docker_back_s3bucket.bucket_arn, export_name="DockerS3BucketARN"+name_suffix)
        CfnOutput(self, "S3 Bucket Name", value=docker_back_s3bucket.bucket_name,
                  export_name="DockerS3BucketName" + name_suffix)
