from aws_cdk import Stack, CfnOutput
from constructs import Construct
from aws_cdk import (
    aws_iam as iam,
)
from front_main.front_main_stack.front_main_s3_stack import FrontMainS3
from front_main.front_main_stack.front_main_cloudfront_stack import FrontMainCLoudfront
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

        codebuild_policy_main = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    actions=["s3:PutObject", "s3:GetObject", "s3:ListBucket"],
                    effect=iam.Effect.ALLOW,
                    resources=[FrontMainS3.bucket_main.bucket_arn, f"{FrontMainS3.bucket_main.bucket_arn}/*", FrontMainS3.bucket_main.bucket_arn, FrontMainS3.bucket_main.bucket_arn + "*"],
                )
            ]
        )

        cloudfront_policy_main = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=["cloudfront:*"],
                    resources=[f"arn:aws:cloudfront:::{os.getenv('ACCOUNT_ID')}:distribution/{FrontMainCLoudfront.distribution_main}"]
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
        CfnOutput(self, "DistributionIDExport", value=FrontMainCLoudfront.distribution_main, export_name="DistributionIDMain")
        CfnOutput(self, "CodeBuildRoleArnExport", value=codebuild_role_arn_main, export_name="CodeBuildRoleArnMain")

