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

class FrontInfraMain(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        existing_managed_policy_arn = "arn:aws:iam::aws:policy/CloudFrontFullAccess"

        existing_policy = iam.ManagedPolicy.from_managed_policy_arn(
            self,
            "ExistingPolicy",
            existing_managed_policy_arn
        )

        bucket_main = s3.Bucket(
            self,
            "bucket-front-main-kryvobok",
            bucket_name="bucket-front-main-kryvobok",
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        distribution_main = cloudfront.Distribution(
            self,
            "cloudfrontdistributionmain",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(bucket_main),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
            default_root_object="index.html",
        )

        codebuild_policy_main = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    actions=["s3:PutObject", "s3:GetObject", "s3:ListBucket"],
                    effect=iam.Effect.ALLOW,
                    resources=[bucket_main.bucket_arn, f"{bucket_main.bucket_arn}/*",bucket_main.bucket_arn, bucket_main.bucket_arn + "*"],
                )
            ]
        )

        distribution_id = distribution_main.distribution_id
        cloudfront_policy_main = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=["cloudfront:*"],
                    resources=[f"arn:aws:cloudfront:::{os.getenv('ACCOUNT_ID')}:distribution/{distribution_id}"]
                )
            ]
        )

        codebuild_role_main = iam.Role(
            self,
            "CodeBuildRoleMain",
            assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"),
            inline_policies={
                "CodeBuildPolicyMain": codebuild_policy_main,
                "CloudFrontCreateInvalidationPolicyMain": cloudfront_policy_main,
            },
        )
        codebuild_role_main.add_managed_policy(existing_policy)

        codebuild_role_arn_main = codebuild_role_main.role_arn
        distribution_id = distribution_main.distribution_id
        CfnOutput(self, "DistributionIDExport", value=distribution_id, export_name="DistributionIDMain")
        CfnOutput(self, "CodeBuildRoleArnExport", value=codebuild_role_arn_main, export_name="CodeBuildRoleArnMain")
        CfnOutput(self, "CloudFrontURL", value="none")
        CfnOutput(self, "S3 Bucket", value=bucket_main.bucket_arn)
