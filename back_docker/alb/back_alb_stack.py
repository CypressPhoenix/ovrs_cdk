from aws_cdk import (
    aws_elasticloadbalancingv2 as elbv2,
    Fn,
    CfnOutput,
    Stack,
    aws_ec2
)
from utils.environment import get_name_suffix
from constructs import Construct

class ALB(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        name_suffix = get_name_suffix()
        vpc_id = Fn.import_value("BackDockerVPCID" + name_suffix)
        vpc = aws_ec2.Vpc(self, "BackDockerVPC" + name_suffix, vpc_id=vpc_id)

        target_group = elbv2.ApplicationTargetGroup(
            self,
            "MyTargetGroup"+name_suffix,
            port=80,
            vpc=vpc,
            target_type=elbv2.TargetType.IP
        )
        alb = elbv2.ApplicationLoadBalancer(
            self,
            "BackDockerALB"+name_suffix,
            vpc=vpc,
            internet_facing=True
        )

        listener = alb.add_listener(
            "Listener"+name_suffix,
            port=80,
            open=True
        )

        listener.add_action(
            "ForwardToTargetGroup"+name_suffix,
            action=elbv2.ListenerAction.forward(target_group),
            priority=1
        )

        listener.add_action(
            "RedirectToHTTPS"+name_suffix,
            action=elbv2.ListenerAction.redirect(
                port="443",
                protocol=elbv2.Protocol.HTTPS,
                permanent=True
            ),
            priority=2
        )

        alb_dns_name = alb.load_balancer_dns_name
        CfnOutput(self, "ALBDNSNameOutput" + name_suffix, value=alb_dns_name, export_name="MyALBDNSName"+name_suffix)
        CfnOutput(self, "TargetGroupArnOutput"+name_suffix, value=target_group.target_group_arn, export_name="MyTargetGroupArn"+name_suffix)
