from aws_cdk import Stack, aws_ecs, CfnOutput, aws_iam, aws_ec2
from constructs import Construct
from utils.environment import get_name_suffix
from aws_cdk import Fn
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_ecs as ecs

class ECS(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        name_suffix = get_name_suffix()
        ecr_uri = Fn.import_value("ECRRepositoryUriTag" + name_suffix)
        docker_s3 = Fn.import_value("DockerS3BucketARN"+name_suffix)
        container_image = aws_ecs.ContainerImage.from_registry(ecr_uri)
        certificate_arn=("arn:aws:acm:eu-west-1:666398651410:certificate/5188490e-5605-4856-980e-eafc323d2717")
        certificate = acm.Certificate.from_certificate_arn(self, "Certificate", certificate_arn)

        cluster = aws_ecs.Cluster(
            self,
            "Cluster"+name_suffix,
        )

        cluster.add_capacity(
            "DockerAutoScalingGroupCapacity"+name_suffix,
            instance_type=aws_ec2.InstanceType("t2.small"),
            desired_capacity=1
        )

        task_execution_role = aws_iam.Role(
            self,
            "TaskExecutionRole"+name_suffix,
            assumed_by=aws_iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            description="Role for the ECS task to access ECR and S3",
        )
        task_def_role = aws_iam.Role(
            self,
            "TaskDefRole"+name_suffix,
            assumed_by=aws_iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            description="Role for the ECS task Def to access ECR and S3",
        )


        s3_access_policy = aws_iam.PolicyStatement(
            actions=[
                 "s3:*",
                "s3-object-lambda:*"
            ],
            resources=["*"],
        )
        task_execution_role.add_to_policy(s3_access_policy)

        task_execution_role.add_to_policy(
            aws_iam.PolicyStatement(
                actions=["ecr:GetDownloadUrlForLayer",
                         "ecr:BatchGetImage",
                         "ecr:BatchCheckLayerAvailability",
                         "ecr:GetAuthorizationToken",
                         "logs:CreateLogGroup",
                         "logs:CreateLogStream",
                         "logs:PutLogEvents",
                         ],

                resources=["*"],
            )
        )
        task_definition = aws_ecs.Ec2TaskDefinition(
            self,
            "TaskDef"+name_suffix,
            execution_role=task_execution_role,
        )

        port_mapping = aws_ecs.PortMapping(
            container_port=3000,
            host_port=0,
            protocol=aws_ecs.Protocol.TCP,
        )
        task_definition.add_container(
            "DockerContainer" + name_suffix,
            image=container_image,
            memory_limit_mib=512,
            cpu=256,
            port_mappings=[port_mapping],
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix="EventDemo",
                mode=ecs.AwsLogDriverMode.NON_BLOCKING,
            )
        )

        ecs_service = aws_ecs.Ec2Service(
            self, "Service"+name_suffix,
            cluster=cluster,
            task_definition=task_definition,
        )

        # Create an Application Load Balancer
        alb = elbv2.ApplicationLoadBalancer(
            self,
            "BackDockerALB" + name_suffix,
            internet_facing=True,
            vpc=cluster.vpc
        )

        target_group = elbv2.ApplicationTargetGroup(
            self,
            "TargetGroup"+name_suffix,
            port=80,
            protocol=elbv2.ApplicationProtocol.HTTP,  # Use ApplicationProtocol
            vpc=cluster.vpc,
        )
        alb_dns_name = alb.load_balancer_dns_name
        ecs_target = ecs_service

        # Привяжите целевой объект к Application Target Group
        ecs_target.attach_to_application_target_group(target_group)

        listener = alb.add_listener("HttpsListener"+name_suffix,
            port=443,
            protocol=elbv2.ApplicationProtocol.HTTPS,
            certificates=[certificate],
            default_target_groups=[target_group],
        )

        task_definition.execution_role.add_to_policy(s3_access_policy)

        CfnOutput(self, "ECSClusterOutput", value=cluster.cluster_name, export_name="ECSClusterOutput"+name_suffix)
        CfnOutput(self, "ECSServiceOutput", value=ecs_service.service_name, export_name="ECSServiceOutput"+name_suffix)
        CfnOutput(self, "ALBDnsName", value=alb_dns_name, export_name="ALBDnsName" + name_suffix)
