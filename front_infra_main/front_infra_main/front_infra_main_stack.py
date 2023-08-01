from aws_cdk import Stack, RemovalPolicy, CfnOutput
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_cloudfront as cloudfront
from constructs import Construct


class FrontInfraMain(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        bucket = s3.Bucket(
            self,
            "BucketForFrontEndMain",
        )

        distribution = cloudfront.CloudFrontWebDistribution(
            self,
            "CloudFrontForFrontEnd",
            origin_configs=[
                cloudfront.SourceConfiguration(
                    s3_origin_source=cloudfront.S3OriginConfig(s3_bucket_source=bucket),
                    behaviors=[cloudfront.Behavior(is_default_behavior=True)],
                )
            ]
        )

        CfnOutput(self, "CloudFrontURL", value="ovrsfront.com")