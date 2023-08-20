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


class Dockerain(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        connection_arn = os.environ.get("CONNECTION_ARN")
        git_branch = os.environ.get("GIT_BRANCH_MAIN")
        git_repo_name = os.environ.get("GIT_REPO_NAME_DOCKER")
        git_repo_owner = os.environ.get("GIT_REPO_OWNER")


        backdockermainpipeline = codepipeline.Pipeline(self, "BackMainDocker", pipeline_name="BackMainDocker",)

        source_output = codepipeline.Artifact()
        build_output = codepipeline.Artifact()

        github_source_action_main = codepipeline_actions.CodeStarConnectionsSourceAction(
            action_name="GitHubSourceMainDocker",
            owner=git_repo_owner,
            repo=git_repo_name,
            branch=git_branch,
            connection_arn=connection_arn,
            output=source_output,
            trigger_on_push=True,
        )

        backdockermainpipeline.add_stage(stage_name="SourceMainDocker", actions=[github_source_action_main])

        codebuild_role_arn_main = Fn.import_value("CodeBuildRoleArnMain")

        project_main = codebuild.PipelineProject(
            self,
            "BuildMainDocker",
            build_spec=codebuild.BuildSpec.from_source_filename("buildspec.yml"),
            environment=codebuild.BuildEnvironment(
                build_image=LinuxBuildImage.from_code_build_image_id("aws/codebuild/standard:7.0")
            ),
            role=docker_role,
        )

        build_action_main_Docker = codepipeline_actions.CodeBuildAction(
            action_name="BuildActionMainDocker",
            input=source_output,
            project=project_main,
            outputs=[build_output],

        )

        backdockermainpipeline.add_stage(stage_name="BuildMainSDocker", actions=[build_action_main_Docker])

