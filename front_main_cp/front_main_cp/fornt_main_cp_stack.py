from aws_cdk import (
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codebuild as codebuild,
    Stack,
    RemovalPolicy,
)
import aws_cdk.aws_s3 as s3
from constructs import Construct
import os
from dotenv import load_dotenv
from aws_cdk.aws_codebuild import LinuxBuildImage

load_dotenv()
class FrontMain(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        connection_arn = os.environ.get("CONNECTION_ARN")
        git_branch = os.environ.get("GIT_BRANCH_MAIN")
        git_repo_name = os.environ.get("GIT_REPO_NAME")
        git_repo_owner = os.environ.get("GIT_REPO_OWNER")

        frontmainpipeline = codepipeline.Pipeline(self, "FrontMain", pipeline_name="FrontMain",)

        source_output = codepipeline.Artifact()
        build_output = codepipeline.Artifact()

        github_source_action = codepipeline_actions.CodeStarConnectionsSourceAction(
            action_name="GitHubSourceMain",
            owner=git_repo_owner,
            repo=git_repo_name,
            branch=git_branch,
            connection_arn=connection_arn,
            output=source_output,
            trigger_on_push=True,
        )

        frontmainpipeline.add_stage(stage_name="SourceMain", actions=[github_source_action])

        project = codebuild.PipelineProject(
            self,
            "BuildMain",
            build_spec=codebuild.BuildSpec.from_source_filename("buildspec.yml"),
            environment=codebuild.BuildEnvironment(
                build_image=LinuxBuildImage.from_code_build_image_id("aws/codebuild/standard:4.0")
            ),
        )

        build_action = codepipeline_actions.CodeBuildAction(
            action_name="BuildActionMain",
            input=source_output,
            project=project,
            outputs=[build_output],
        )

        frontmainpipeline.add_stage(stage_name="BuildMain", actions=[build_action])