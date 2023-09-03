from aws_cdk import Stack, RemovalPolicy, Fn, CfnOutput
from aws_cdk import aws_dynamodb as dynamodb
from constructs import Construct
from utils.environment import get_name_suffix

class DatabaseStackDev(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        name_suffix = get_name_suffix()

        columns_table = dynamodb.Table(
            self,
            "ColumnsTable",
            table_name="adavydova-columns"+name_suffix,
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
            table_name="adavydova-cards"+name_suffix,
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
        columns_table_arn = columns_table.table_arn
        cards_table_arn = cards_table.table_arn
        columns_table_name = columns_table.table_name
        cards_table_name = cards_table.table_name
        CfnOutput(self, "CardsTableArnDevExport", value=cards_table_arn, export_name="CardsTableArn"+name_suffix)
        CfnOutput(self, "ColumnsTableArnDevExport", value=columns_table_arn, export_name="ColumnsTableArn"+name_suffix)
        CfnOutput(self, "CardsTableNameDevExport", value=cards_table_name, export_name="CardsTableName"+name_suffix)
        CfnOutput(self, "ColumnsTableNameDevExport", value=columns_table_name, export_name="ColumnsTableName"+name_suffix)