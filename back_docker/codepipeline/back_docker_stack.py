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
        git_repo_name = os.environ.get("GIT_REPO_NAME")
        git_repo_owner = os.environ.get("GIT_REPO_OWNER")
        alb_dns_name = Fn.import_value("MyALBDNSName")
        name_suffix = get_name_suffix()

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

        docker_codebuild = codebuild.PipelineProject(
            self,
            "DockerBuild" + name_suffix,
            build_spec=codebuild.BuildSpec.from_source_filename("buildspec.yml"),
            environment=codebuild.BuildEnvironment(
                build_image=LinuxBuildImage.from_code_build_image_id("aws/codebuild/standard:7.0")
            ),
        )

        build_action = codepipeline_actions.CodeBuildAction(
            action_name="BuildActionDocker" + name_suffix,
            input=source_output,
            project=docker_codebuild,
            outputs=[build_output],
            environment_variables={
                "ENV": codebuild.BuildEnvironmentVariable(value=os.environ.get("ENV")),
                "Endpoint": codebuild.BuildEnvironmentVariable(value=alb_dns_name)
            },
        )

        dockerpipeline.add_stage(stage_name="DockerBuild" + name_suffix, actions=[build_action])

