from aws_cdk import Stack, RemovalPolicy, CfnOutput
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_cloudfront as cloudfront
from constructs import Construct
import aws_cdk.aws_iam as iam
from aws_cdk import (
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_certificatemanager as acm,
    aws_route53 as route53,
    aws_route53_targets as targets,
    aws_iam as iam,
    aws_ssm as ssm,
    RemovalPolicy
)
import os
from dotenv import load_dotenv
load_dotenv()

class FrontInfraMain(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        bucket_dev = s3.Bucket(
            self,
            "bucketforfrontdev",
            bucket_name="bucketbforfrontdev",
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        # Create a CloudFront distribution_main.
        distribution_dev = cloudfront.Distribution(
            self,
            "cloudfrontdistributiondev",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(bucket_dev),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
            default_root_object="index.html",
        )

        codebuild_policy_dev = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    actions=["s3:PutObject", "s3:GetObject", "s3:ListBucket"],
                    effect=iam.Effect.ALLOW,
                    resources=[bucket_dev.bucket_arn, bucket_dev.bucket_arn + "/*", bucket_dev.bucket_arn, bucket_dev.bucket_arn + "*"],

                )
            ]
        )
        distribution_id=distribution_dev.distribution_id
        cloudfront_policy_dev = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=["cloudfront:CreateInvalidation"],
                    resources=[f"arn:aws:cloudfront::{os.getenv('ACCOUNT_ID')}:distribution_main/{distribution_id}"]
                )
            ]
        )

        # Создаем IAM роль для CodeBuild
        codebuild_role_dev = iam.Role(
            self,
            "CodeBuildRoleDev",
            assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"),
            inline_policies={
                "CodeBuildPolicyDev": codebuild_policy_dev,
                "CloudFrontCreateInvalidationPolicyDev": cloudfront_policy_dev,
            },
        )

        # Экспортируем роль IAM для использования в других стеках
        codebuild_role_arn_dev = codebuild_role_dev.role_arn
        CfnOutput(self, "CodeBuildRoleArnExport", value=codebuild_role_arn_dev, export_name="CodeBuildRoleArnDev")
        CfnOutput(self, "CloudFrontURL", value="none")
        CfnOutput(self, "S3 Bucket", value=bucket_dev.bucket_arn)
