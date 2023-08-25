from aws_cdk import Stack, CfnOutput
from constructs import Construct
from aws_cdk import (
    aws_iam as iam,
    Fn
)
from front.front_cloudfront_stack.front_cloudfront_stack import FrontMainCLoudfront
import os
from dotenv import load_dotenv
load_dotenv()

class FrontIAM(Stack):
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

        front_s3_bucket_arn = Fn.import_value("S3BucketArn"+name_suffix)
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
                    resources=[front_s3_bucket_arn, f"{front_s3_bucket_arn}/*", front_s3_bucket_arn, front_s3_bucket_arn + "*"],
                )
            ]
        )

        cloudfront_policy_main = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=["cloudfront:*"],
                    resources=[f"arn:aws:cloudfront:::{os.getenv('ACCOUNT_ID')}:distribution/{self.distribution_id}"]
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

