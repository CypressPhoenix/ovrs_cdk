from aws_cdk import Stack, RemovalPolicy, Fn, CfnOutput
from aws_cdk import aws_dynamodb as dynamodb
from constructs import Construct

class DatabaseStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        columns_table = dynamodb.Table(
            self,
            "ColumnsTable",
            table_name="adavydova-columns",
            partition_key=dynamodb.Attribute(
                name="columnID",
                type=dynamodb.AttributeType.STRING
            ),
            read_capacity=1,
            write_capacity=1,
            removal_policy=RemovalPolicy.DESTROY  # Be cautious with this setting in production
        )

        cards_table = dynamodb.Table(
            self,
            "CardsTable",
            table_name="adavydova-cards",
            partition_key=dynamodb.Attribute(
                name="cardID",
                type=dynamodb.AttributeType.STRING
            ),
            read_capacity=1,
            write_capacity=1,
            removal_policy=RemovalPolicy.DESTROY  # Be cautious with this setting in production
        )

        # Export the tables' ARNs for use in other stacks or applications
        columns_table_arn_main = columns_table.table_arn
        cards_table_arn_main = cards_table.table_arn
        CfnOutput(self, "CardsTableArnMainExport", value=cards_table_arn_main, export_name="CardsTableArnMain")
        CfnOutput(self, "ColumnsTableArnMainExport", value=columns_table_arn_main, export_name="ColumnsTableArnMain")