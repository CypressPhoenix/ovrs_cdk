from aws_cdk import (
    aws_ec2,
    aws_elasticloadbalancingv2 as elbv2,
    core
)

class ALBStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc: aws_ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Создание Amazon Application Load Balancer (ALB)
        alb = elbv2.ApplicationLoadBalancer(
            self,
            "ALB",
            vpc=vpc,
            internet_facing=True
        )

        self.alb = alb