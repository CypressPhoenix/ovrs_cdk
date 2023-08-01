from aws_cdk import (
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codebuild as codebuild,
    Stack,
)

from constructs import Construct
import os
from dotenv import load_dotenv
from aws_cdk.aws_codebuild import LinuxBuildImage

load_dotenv()
class FrontDev(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        connection_arn = os.environ.get("CONNECTION_ARN")
        git_branch = os.environ.get("GIT_BRANCH_DEV")
        git_repo_name = os.environ.get("GIT_REPO_NAME")
        git_repo_owner = os.environ.get("GIT_REPO_OWNER")

        frontdevpipeline = codepipeline.Pipeline(self, "FrontDev", pipeline_name="FrontDev",)

        source_output = codepipeline.Artifact()
        build_output = codepipeline.Artifact()

        github_source_action = codepipeline_actions.CodeStarConnectionsSourceAction(
            action_name="GitHubSourceDev",
            owner=git_repo_owner,
            repo=git_repo_name,
            branch=git_branch,
            connection_arn=connection_arn,
            output=source_output,
            trigger_on_push=True,
        )

        frontdevpipeline.add_stage(stage_name="SourceDev", actions=[github_source_action])

        project = codebuild.PipelineProject(
            self,
            "BuildDev",
            build_spec=codebuild.BuildSpec.from_source_filename("buildspec.yml"),
            environment=codebuild.BuildEnvironment(
                build_image=LinuxBuildImage.from_code_build_image_id("aws/codebuild/standard:4.0")
            ),
        )

        build_action = codepipeline_actions.CodeBuildAction(
            action_name="BuildActionDev",
            input=source_output,
            project=project,
            outputs=[build_output],
        )

        frontdevpipeline.add_stage(stage_name="BuildDev", actions=[build_action])