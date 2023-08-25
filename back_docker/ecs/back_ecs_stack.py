from aws_cdk import (
    aws_ecs,
    Stack,
)
from constructs import Construct
import os
from dotenv import load_dotenv

load_dotenv()

class ECS(Stack):
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

        ecs_cluster = aws_ecs.Cluster(
            self,
            "ECSCluster"+name_suffix,
            cluster_name="ecscluster"+name_suffix
        )