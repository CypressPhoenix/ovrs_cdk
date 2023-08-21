from aws_cdk import Stack, RemovalPolicy, Fn, CfnOutput
from aws_cdk import aws_dynamodb as dynamodb
from constructs import Construct

class DatabaseStackTest(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        columns_table = dynamodb.Table(
            self,
            "ColumnsTable",
            table_name="adavydova-columns_test",
            partition_key=dynamodb.Attribute(
                name="columnID",
                type=dynamodb.AttributeType.STRING
            ),
            read_capacity=1,
            write_capacity=1,
            removal_policy=RemovalPolicy.DESTROY  # Be cautious with this setting in production
        )
        columns_table.add_global_secondary_index(
            index_name='columnsByIndex',
            partition_key=dynamodb.Attribute(
                name='columnIndex',
                type=dynamodb.AttributeType.NUMBER
            ),
            projection_type=dynamodb.ProjectionType.ALL,
            read_capacity=1,
            write_capacity=1
        )

        cards_table = dynamodb.Table(
            self,
            "CardsTable",
            table_name="adavydova-cards-test",
            partition_key=dynamodb.Attribute(
                name="cardID",
                type=dynamodb.AttributeType.STRING
            ),
            read_capacity=1,
            write_capacity=1,
            removal_policy=RemovalPolicy.DESTROY  # Be cautious with this setting in production
        )
        cards_table.add_global_secondary_index(
            index_name="cardsByColumnIdAndIndex",
            partition_key=dynamodb.Attribute(
                name="columnID",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name='cardIndex',
                type=dynamodb.AttributeType.NUMBER
            ),
            read_capacity=1,
            write_capacity=1,
            projection_type=dynamodb.ProjectionType.ALL
        )

        # Export the tables' ARNs for use in other stacks or applications
        columns_table_arn_test = columns_table.table_arn
        cards_table_arn_test = cards_table.table_arn
        columns_table_name_test = columns_table.table_name
        cards_table_name_test = cards_table.table_name
        CfnOutput(self, "CardsTableArnTestExport", value=cards_table_arn_test, export_name="CardsTableArnTest")
        CfnOutput(self, "ColumnsTableArnTestExport", value=columns_table_arn_test, export_name="ColumnsTableArnTest")
        CfnOutput(self, "CardsTableNameTestExport", value=cards_table_name_test, export_name="CardsTableNameTest")
        CfnOutput(self, "ColumnsTableNameTestExport", value=columns_table_name_test, export_name="ColumnsTableNameTest")