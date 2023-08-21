from aws_cdk import Stack, CfnOutput
from constructs import Construct
from aws_cdk import (
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_iam as iam,
)
from front_main.front_main_stack.front_main_s3_stack import FrontMainS3
from dotenv import load_dotenv
load_dotenv()

class FrontMainCLoudfront(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        existing_managed_policy_arn = "arn:aws:iam::aws:policy/CloudFrontFullAccess"

        existing_policy = iam.ManagedPolicy.from_managed_policy_arn(
            self,
            "ExistingPolicy",
            existing_managed_policy_arn
        )

        distribution_main = cloudfront.Distribution(
            self,
            "cloudfrontdistributionmain",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(FrontMainS3.bucket_main),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
            default_root_object="index.html",
        )

        distribution_id = distribution_main.distribution_id
        CfnOutput(self, "DistributionIDExport", value=distribution_id, export_name="DistributionIDMain")

