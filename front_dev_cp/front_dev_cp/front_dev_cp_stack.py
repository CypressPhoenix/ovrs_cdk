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
import aws_cdk.aws_iam as iam

load_dotenv()


class FrontDev(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        connection_arn = os.environ.get("CONNECTION_ARN")
        git_branch = os.environ.get("GIT_BRANCH_DEV")
        git_repo_name = os.environ.get("GIT_REPO_NAME")
        git_repo_owner = os.environ.get("GIT_REPO_OWNER")
        distribution_id = Fn.import_value("DistributionIDDev")

        frontdevpipeline = codepipeline.Pipeline(self, "FrontDev", pipeline_name="FrontDev",)

        source_output = codepipeline.Artifact()
        build_output = codepipeline.Artifact()

        github_source_action_Dev = codepipeline_actions.CodeStarConnectionsSourceAction(
            action_name="GitHubSourceDev",
            owner=git_repo_owner,
            repo=git_repo_name,
            branch=git_branch,
            connection_arn=connection_arn,
            output=source_output,
            trigger_on_push=True,
        )

        frontdevpipeline.add_stage(stage_name="SourceDev", actions=[github_source_action_Dev])

        codebuild_role_arn_dev = Fn.import_value("CodeBuildRoleArnDev")

        project_dev = codebuild.PipelineProject(
            self,
            "BuildDev",
            build_spec=codebuild.BuildSpec.from_source_filename("buildspec.yml"),
            environment=codebuild.BuildEnvironment(
                build_image=LinuxBuildImage.from_code_build_image_id("aws/codebuild/standard:7.0")
            ),
            role=iam.Role.from_role_arn(self, "ImportedCodeBuildRole", role_arn=codebuild_role_arn_dev),
        )

        build_action_dev = codepipeline_actions.CodeBuildAction(
            action_name="BuildActionDev",
            input=source_output,
            project=project_dev,
            outputs=[build_output],
            environment_variables={
                "CL_FRONT_DIST_ID": codebuild.BuildEnvironmentVariable(value=distribution_id),
            },
        )

        frontdevpipeline.add_stage(stage_name="BuildDev", actions=[build_action_dev])
