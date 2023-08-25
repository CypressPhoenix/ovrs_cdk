from aws_cdk import (
    aws_ec2,
    Stack,

)
from constructs import Construct
class BackVPC(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = aws_ec2.Vpc(
            self,
            "MyVPC",
            max_azs=2,
            cidr="10.0.0.0/16",  # Задайте подходящий CIDR для вашей сети
            subnet_configuration=[
                aws_ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=aws_ec2.SubnetType.PUBLIC
                ),
                aws_ec2.SubnetConfiguration(
                    name="Private",
                    subnet_type=aws_ec2.SubnetType.PRIVATE
                )
            ],
            nat_gateways=1  # Количество NAT Gateways для приватных подсетей
        )

        self.vpc = vpc