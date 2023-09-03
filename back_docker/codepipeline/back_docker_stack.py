from aws_cdk import (
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codebuild as codebuild,
    Stack,
    Fn
)
from constructs import Construct
from utils.environment import get_name_suffix
import os
from dotenv import load_dotenv
from aws_cdk.aws_codebuild import LinuxBuildImage
import aws_cdk.aws_iam as iam

load_dotenv()


class DockerCP(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        connection_arn = os.environ.get("CONNECTION_ARN")
        git_repo_name = os.environ.get("GIT_REPO_NAME_DOCKER")
        git_repo_owner = os.environ.get("GIT_REPO_OWNER")
        name_suffix = get_name_suffix()
        ecr_uri = Fn.import_value("ECRRepositoryUri" + name_suffix)
        region = os.environ.get("REGION_HOME")
        ecs_cluster_name = Fn.import_value("ECSClusterOutput"+name_suffix)
        ecs_service_name = Fn.import_value("ECSServiceOutput"+name_suffix)
        ACCOUNT_ID=os.environ.get("ACCOUNT_ID")
        ecr = "ecr"+name_suffix
        docker_bucket_name = Fn.import_value("DockerS3BucketName" + name_suffix)

        dockerpipeline = codepipeline.Pipeline(
            self, "DockerCP" + name_suffix, pipeline_name="DockerCP" + name_suffix
        )

        source_output = codepipeline.Artifact()
        build_output = codepipeline.Artifact()

        github_source_action = codepipeline_actions.CodeStarConnectionsSourceAction(
            action_name="GitHubSource" + name_suffix,
            owner=git_repo_owner,
            repo=git_repo_name,
            branch=name_suffix,
            connection_arn=connection_arn,
            output=source_output,
            trigger_on_push=True,
        )

        dockerpipeline.add_stage(stage_name="Source" + name_suffix, actions=[github_source_action])

        codebuild_policy_main = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    actions=[
                    "ecr:GetDownloadUrlForLayer",
                    "ecr:BatchGetImage",
                    "ecr:BatchCheckLayerAvailability",
                    "ecr:PutImage",
                    "ecr:GetAuthorizationToken",
                    "ecr:GetRegistryPolicy",
                    "ecr:GetRepositoryPolicy",
                    "ecr:ListImages",
                    "ecr:DescribeRepositories",
                    "ecr:CreateRepository",
                    "ecr:DeleteRepository",
                    "ecr:PutLifecyclePolicy",
                    "ecr:GetLifecyclePolicy",
                    "ecr:DeleteLifecyclePolicy",
                    "ecr:BatchCheckLayerAvailability",
                    "ecr:CompleteLayerUpload",
                    "ecr:GetAuthorizationToken",
                    "ecr:InitiateLayerUpload",
                    "ecr:PutImage",
                    "ecr:UploadLayerPart",
                    "ecs:UpdateService",
                    "ecs:DescribeServices",
                    "ecs:DescribeTaskDefinition",
                    "ecr:BatchDeleteImage",
                    "ecr:PutImageTagMutability",
                    "ecr:DescribeImages"
                ],
                    effect=iam.Effect.ALLOW,
                    resources=["*"]
                )
            ]
        )

        codebuild_role_docker = iam.Role(
            self,
            "CodeBuildRole"+name_suffix,
            assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"),
            inline_policies={
                "CodeBuildPolicyMain": codebuild_policy_main,
            },
        )

        docker_codebuild = codebuild.PipelineProject(
            self,
            "DockerBuild" + name_suffix,
            build_spec=codebuild.BuildSpec.from_source_filename("buildspec.yml"),
            environment=codebuild.BuildEnvironment(
                build_image=LinuxBuildImage.from_code_build_image_id("aws/codebuild/standard:7.0"),
                privileged=True,  # Добавьте эту строку для включения режима "привилегированного" доступа
            ),
            role=codebuild_role_docker,
        )

        build_action = codepipeline_actions.CodeBuildAction(
            action_name="BuildActionDocker" + name_suffix,
            input=source_output,
            project=docker_codebuild,
            outputs=[build_output],
            environment_variables={
                "ENV": codebuild.BuildEnvironmentVariable(value=os.environ.get("ENV")),
                "REPOSITORY_URI": codebuild.BuildEnvironmentVariable(value=ecr_uri),
                "AWS_DEFAULT_REGION": codebuild.BuildEnvironmentVariable(value=region),
                "IMAGE_REPO_NAME": codebuild.BuildEnvironmentVariable(value=ecr),
                "ECS_SERVICE_NAME": codebuild.BuildEnvironmentVariable(value=ecs_service_name),
                "AWS_ACCOUNT_ID": codebuild.BuildEnvironmentVariable(value=ACCOUNT_ID),
                "IMAGE_TAG": codebuild.BuildEnvironmentVariable(value="latest"),
                "ECS_CLUSTER_NAME":codebuild.BuildEnvironmentVariable(value=ecs_cluster_name),
                "DOCKER_BUCKET_NAME": codebuild.BuildEnvironmentVariable(value=docker_bucket_name)
            },
        )

        dockerpipeline.add_stage(stage_name="DockerBuild" + name_suffix, actions=[build_action])

