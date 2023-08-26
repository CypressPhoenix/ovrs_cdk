from aws_cdk import (
    aws_ecs,
    Stack,
    aws_ec2,
    Fn,
)
from constructs import Construct
from dotenv import load_dotenv
from utils.environment import get_name_suffix

load_dotenv()

class ECS(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        name_suffix = get_name_suffix()
        ecr_uri = Fn.import_value("ECRRepositoryUri" + name_suffix)
        container_image = aws_ecs.ContainerImage.from_registry(ecr_uri)
        target_group_arn = Fn.import_value("MyTargetGroupArn")
        vpc_id = Fn.import_value("BackDockerVPCID" + name_suffix)
        vpc = aws_ec2.Vpc.from_lookup(self, "BackDockerVPC" + name_suffix, vpc_id=vpc_id)
        ecs_cluster = aws_ecs.Cluster(
            self,
            "ECSCluster"+name_suffix,
            cluster_name="ECScluster"+name_suffix,
            vpc=vpc
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
            "DockerBack" + name_suffix,
            image=container_image,
            memory_limit_mib=512
        )

        ecs_service = aws_ecs.Ec2Service(
            self,
            "ServiceECS"+name_suffix,
            cluster=ecs_cluster,
            task_definition=task_definition,
            target_group=target_group_arn
        )

