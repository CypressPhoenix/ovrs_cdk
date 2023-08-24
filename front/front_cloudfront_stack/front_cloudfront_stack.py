from aws_cdk import Stack, CfnOutput
from constructs import Construct
from aws_cdk import (
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_iam as iam,
)
import os
from front.front_stack.front_s3_stack import FrontMainS3
from dotenv import load_dotenv
load_dotenv()

class FrontCLoudfront(Stack):
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

        cloudfront_distribution = cloudfront.Distribution(
            self,
            "cloudfrontdistribution"+name_suffix,
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(FrontMainS3.bucket_main),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
            default_root_object="index.html",
        )

        self.distribution_id = cloudfront_distribution.distribution_id
        distribution_id = cloudfront_distribution.distribution_id
        CfnOutput(self, "DistributionIDExport", value=distribution_id, export_name="DistributionID"+name_suffix)

