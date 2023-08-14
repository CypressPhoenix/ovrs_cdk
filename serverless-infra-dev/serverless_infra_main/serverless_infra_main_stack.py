from aws_cdk import Stack
from constructs import Construct
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_iam as iam
from aws_cdk import Fn

class LambdaDynamoDBTestStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        cloudfront_distribution_id = Fn.import_value("MyCloudFrontDistributionIdMain")
        # Step 1: Create Lambda function
        my_lambda = _lambda.Function(
            self, 'MyLambda',
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler='index.handler',
            code=_lambda.Code.from_asset('lambda'),
        )

        # Step 2: Create DynamoDB table
        my_table = dynamodb.Table(
            self, 'MyTable',
            partition_key=dynamodb.Attribute(
                name='id',
                type=dynamodb.AttributeType.STRING,
            )
        )

        # Step 3: Create API Gateway
        my_api = apigateway.RestApi(
            self, 'MyApi',
            deploy_options={
                "stage_name": "v1"
            }
        )

        my_resource = my_api.root.add_resource('my-resource')
        cloudfront_integration = apigateway.Integration(
            type=apigateway.IntegrationType.HTTP,
            integration_http_method="GET",
            uri=f"https://{cloudfront_distribution_id}.cloudfront.net",
        )
        my_resource.add_method('GET', cloudfront_integration)

        # Step 4: Create IAM role for Lambda to access DynamoDB
        lambda_role = iam.Role(
            self, 'LambdaRole',
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
        )
        my_table.grant_read_write_data(lambda_role)

        # Step 5: Create Lambda integration with API Gateway
        my_resource = my_api.root.add_resource('my-resource')
        my_resource.add_method('GET', apigateway.LambdaIntegration(my_lambda))


