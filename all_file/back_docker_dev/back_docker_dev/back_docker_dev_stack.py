from aws_cdk import (
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codebuild as codebuild,
    Stack,
    Fn
)
from constructs import Construct
import os
from dotenv import load_dotenv
from aws_cdk.aws_codebuild import LinuxBuildImage


load_dotenv()


class DockerDev(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        connection_arn = os.environ.get("CONNECTION_ARN")
        git_branch = os.environ.get("GIT_BRANCH_DEV")
        git_repo_name = os.environ.get("GIT_REPO_NAME_DOCKER")
        git_repo_owner = os.environ.get("GIT_REPO_OWNER")


        backdockerdevpipeline = codepipeline.Pipeline(self, "BackDevDocker", pipeline_name="BackDevDocker",)

        source_output = codepipeline.Artifact()
        build_output = codepipeline.Artifact()
# Create source step
        github_source_action_dev = codepipeline_actions.CodeStarConnectionsSourceAction(
            action_name="GitHubSourceDevDocker",
            owner=git_repo_owner,
            repo=git_repo_name,
            branch=git_branch,
            connection_arn=connection_arn,
            output=source_output,
            trigger_on_push=True,
        )

        backdockerdevpipeline.add_stage(stage_name="SourceDevDocker", actions=[github_source_action_dev])

        codebuild_role_arn_dev = Fn.import_value("CodeBuildRoleArnDev")

        project_dev = codebuild.PipelineProject(
            self,
            "BuildDevDocker",
            build_spec=codebuild.BuildSpec.from_source_filename("buildspec.yml"),
            environment=codebuild.BuildEnvironment(
                build_image=LinuxBuildImage.from_code_build_image_id("aws/codebuild/standard:7.0")
            ),
        )

        build_action_dev_docker = codepipeline_actions.CodeBuildAction(
            action_name="BuildActionDevDocker",
            input=source_output,
            project=project_dev,
            outputs=[build_output],

        )

        backdockerdevpipeline.add_stage(stage_name="BuildDevSDocker", actions=[build_action_dev_docker])

