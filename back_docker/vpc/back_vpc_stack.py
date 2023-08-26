from aws_cdk import (
    Stack,
    aws_ec2,
    CfnOutput
)
from constructs import Construct
from dotenv import load_dotenv
from utils.environment import get_name_suffix

load_dotenv()
class BackVPC(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        name_suffix = get_name_suffix()
        vpc = aws_ec2.Vpc(self, "BackDockerVPC"+name_suffix, max_azs=2)
        vpc_id = vpc.vpc_id

        CfnOutput(self, "BackDockerVPCID"+name_suffix, value=vpc_id, export_name="BackDockerVPCID" + name_suffix)