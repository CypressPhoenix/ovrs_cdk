from constructs import Construct
from aws_cdk import (
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_s3 as s3,
    RemovalPolicy,
    CfnOutput,
    Stack
)
from utils.environment import get_name_suffix
from dotenv import load_dotenv
load_dotenv()

class FrontInfra(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        name_suffix = get_name_suffix()

        s3bucket = s3.Bucket(
            self,
            "bucketfrontkryvobok"+name_suffix,
            bucket_name="bucketfrontkryvobok"+name_suffix,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        cloudfront_distribution = cloudfront.Distribution(
            self,
            "cloudfrontdistribution"+name_suffix,
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(s3bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
            default_root_object="index.html",
        )


        self.distribution_id = cloudfront_distribution.distribution_id
        distribution_id = cloudfront_distribution.distribution_id
        CfnOutput(self, "DistributionIDExport", value=distribution_id, export_name="DistributionID"+name_suffix)
        CfnOutput(self, "S3 Bucket ARN", value=s3bucket.bucket_arn, export_name="S3BucketArn"+name_suffix)
        CfnOutput(self, "S3BucketNameOutput", value=s3bucket.bucket_name, export_name="FrontS3BucketName"+name_suffix)


