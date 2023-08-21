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

class FrontInfraTest(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        existing_managed_policy_arn = "arn:aws:iam::aws:policy/CloudFrontFullAccess"

        existing_policy = iam.ManagedPolicy.from_managed_policy_arn(
            self,
            "ExistingPolicy",
            existing_managed_policy_arn
        )

        bucket_test = s3.Bucket(
            self,
            "bucket-front-test-kryvobok",
            bucket_name="bucket-front-test-kryvobok",
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        distribution_test = cloudfront.Distribution(
            self,
            "cloudfrontdistributiontest",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(bucket_test),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
            default_root_object="index.html",
        )

        codebuild_policy_test = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    actions=["s3:PutObject", "s3:GetObject", "s3:ListBucket"],
                    effect=iam.Effect.ALLOW,
                    resources=[bucket_test.bucket_arn, f"{bucket_test.bucket_arn}/*",bucket_test.bucket_arn, bucket_test.bucket_arn + "*"],
                )
            ]
        )

        distribution_id = distribution_test.distribution_id
        cloudfront_policy_test = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=["cloudfront:*"],
                    resources=[f"arn:aws:cloudfront:::{os.getenv('ACCOUNT_ID')}:distribution/{distribution_id}"]
                )
            ]
        )

        codebuild_role_test = iam.Role(
            self,
            "CodeBuildRoleTest",
            assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"),
            inline_policies={
                "CodeBuildPolicyTest": codebuild_policy_test,
                "CloudFrontCreateInvalidationPolicyTest": cloudfront_policy_test,
            },
        )
        codebuild_role_test.add_managed_policy(existing_policy)

        codebuild_role_arn_test = codebuild_role_test.role_arn
        distribution_id = distribution_test.distribution_id
        bucket_name = bucket_test.bucket_name
        CfnOutput(self, "DistributionIDExport", value=distribution_id, export_name="DistributionIDTest")
        CfnOutput(self, "CodeBuildRoleArnExport", value=codebuild_role_arn_test, export_name="CodeBuildRoleArnTest")
        CfnOutput(self, "CloudFrontURL", value="none")
        CfnOutput(self, "S3 Bucket", value=bucket_test.bucket_arn)
        CfnOutput(self, "s3 Bucket Name", value=bucket_name, export_name="BucketNameTest")
