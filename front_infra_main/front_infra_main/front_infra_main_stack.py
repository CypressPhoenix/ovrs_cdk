from aws_cdk import Stack, RemovalPolicy, CfnOutput
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_cloudfront as cloudfront
from constructs import Construct
import aws_cdk.aws_iam as iam


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

        codebuild_policy = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    actions=["s3:PutObject", "s3:GetObject", "s3:ListBucket"],
                    effect=iam.Effect.ALLOW,
                    resources=[bucket.bucket_arn, bucket.bucket_arn + "/*", bucket.bucket_arn, bucket.bucket_arn + "*"],

                )
            ]
        )

        # Создаем IAM роль для CodeBuild
        codebuild_role = iam.Role(
            self,
            "CodeBuildRole",
            assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"),
            inline_policies={"CodeBuildPolicy": codebuild_policy},
        )

        # Экспортируем роль IAM для использования в других стеках
        codebuild_role_arn = codebuild_role.role_arn
        CfnOutput(self, "CodeBuildRoleArnExport", value=codebuild_role_arn, export_name="CodeBuildRoleArn")

        CfnOutput(self, "CloudFrontURL", value="ovrsfront.com")
        CfnOutput(self, "S3 Bucket", value=bucket.bucket_arn)
