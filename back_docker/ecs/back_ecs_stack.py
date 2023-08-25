from aws_cdk import (
    aws_ecs,
    Stack,
    aws_ec2
)
from constructs import Construct
from back_docker.ecr.back_ecr_stack import ECR
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
            cluster_name="ECScluster"+name_suffix
        )

        ecs_cluster.add_capacity(
            "DockerBack"+name_suffix,
            instance_type=aws_ec2.InstanceType("t2.micro"),
            desired_capacity=1
        )

        task_definition = aws_ecs.Ec2TaskDefinition(
            self,
            "DockerBackTask"+name_suffix
        )

        task_definition.add_container(
            "DockerBack"+name_suffix,
            image=ECR.docker_back_repository.repository_uri_for_tag("latest"),
            memory_limit_mi_b=512
        )

        ecs_service = aws_ecs.Ec2Service(
            self,
            "Service",
            cluster=ecs_cluster,
            task_definition=task_definition
        )