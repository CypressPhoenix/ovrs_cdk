from aws_cdk import Stack, CfnOutput
from constructs import Construct
from aws_cdk import (
    aws_iam as iam,
    Fn
)
import os
from dotenv import load_dotenv
from utils.environment import get_name_suffix
load_dotenv()

class FrontIAM(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        name_suffix = get_name_suffix()

        front_s3_bucket_arn = Fn.import_value("S3BucketArn"+name_suffix)
        distribution_id = Fn.import_value("DistributionID"+name_suffix)
        existing_managed_policy_arn = "arn:aws:iam::aws:policy/CloudFrontFullAccess"

        existing_policy = iam.ManagedPolicy.from_managed_policy_arn(
            self,
            "ExistingPolicy",
            existing_managed_policy_arn
        )

        codebuild_policy = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    actions=["s3:PutObject", "s3:GetObject", "s3:ListBucket"],
                    effect=iam.Effect.ALLOW,
                    resources=[front_s3_bucket_arn, f"{front_s3_bucket_arn}/*", front_s3_bucket_arn, front_s3_bucket_arn + "*"],
                )
            ]
        )

        cloudfront_policy = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=["cloudfront:*"],
                    resources=[f"arn:aws:cloudfront:::{os.getenv('ACCOUNT_ID')}:distribution/{distribution_id}"]
                )
            ]
        )

        codebuild_role = iam.Role(
            self,
            "CodeBuildRole"+name_suffix,
            assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"),
            inline_policies={
                "CodeBuildPolicy": codebuild_policy,
                "CloudFrontCreateInvalidationPolicy": cloudfront_policy,
            },
        )
        codebuild_role.add_managed_policy(existing_policy)
        codebuild_role_arn = codebuild_role.role_arn
        CfnOutput(self, "CodeBuildRoleArnExport", value=codebuild_role_arn, export_name="CodeBuildRoleArn"+name_suffix)

