from aws_cdk import Stack, CfnOutput
from constructs import Construct
from aws_cdk import (
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_iam as iam,
    RemovalPolicy
)
import os
from dotenv import load_dotenv
load_dotenv()

class FrontInfraDev(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        existing_managed_policy_arn = "arn:aws:iam::aws:policy/CloudFrontFullAccess"

        existing_policy = iam.ManagedPolicy.from_managed_policy_arn(
            self,
            "ExistingPolicy",
            existing_managed_policy_arn
        )

        bucket_dev = s3.Bucket(
            self,
            "bucket-front-dev-kryvobok",
            bucket_name="bucket-front-dev-kryvobok",
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

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
                    resources=[bucket_dev.bucket_arn, f"{bucket_dev.bucket_arn}/*",bucket_dev.bucket_arn, bucket_dev.bucket_arn + "*"],
                )
            ]
        )

        distribution_id = distribution_dev.distribution_id
        cloudfront_policy_dev = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=["cloudfront:*"],
                    resources=[f"arn:aws:cloudfront:::{os.getenv('ACCOUNT_ID')}:distribution/{distribution_id}"]
                )
            ]
        )

        codebuild_role_dev = iam.Role(
            self,
            "CodeBuildRoleDev",
            assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"),
            inline_policies={
                "CodeBuildPolicyDev": codebuild_policy_dev,
                "CloudFrontCreateInvalidationPolicyDev": cloudfront_policy_dev,
            },
        )
        codebuild_role_dev.add_managed_policy(existing_policy)

        codebuild_role_arn_dev = codebuild_role_dev.role_arn
        distribution_id = distribution_dev.distribution_id
        CfnOutput(self, "DistributionIDExport", value=distribution_id, export_name="DistributionIDDev")
        CfnOutput(self, "CodeBuildRoleArnExport", value=codebuild_role_arn_dev, export_name="CodeBuildRoleArnDev")
        CfnOutput(self, "CloudFrontURL", value="none")
        CfnOutput(self, "S3BucketARN", value=bucket_dev.bucket_arn)
        CfnOutput(self, "S3BucketName", value=bucket_dev.bucket_name, export_name="S3BucketName")
