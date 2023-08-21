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


class FrontMain(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        connection_arn = os.environ.get("CONNECTION_ARN")
        git_branch = os.environ.get("GIT_BRANCH_MAIN")
        git_repo_name = os.environ.get("GIT_REPO_NAME")
        git_repo_owner = os.environ.get("GIT_REPO_OWNER")
        distribution_id = Fn.import_value("DistributionIDMain")

        pipeline_name_suffix = git_branch.capitalize()

        frontpipeline = codepipeline.Pipeline(self, "Front" + pipeline_name_suffix, pipeline_name="Front" + pipeline_name_suffix)

        source_output = codepipeline.Artifact()
        build_output = codepipeline.Artifact()

        github_source_action = codepipeline_actions.CodeStarConnectionsSourceAction(
            action_name="GitHubSource" + pipeline_name_suffix,
            owner=git_repo_owner,
            repo=git_repo_name,
            branch=git_branch,
            connection_arn=connection_arn,
            output=source_output,
            trigger_on_push=True,
        )

        frontpipeline.add_stage(stage_name="Source" + pipeline_name_suffix, actions=[github_source_action])

        codebuild_role_arn = Fn.import_value("CodeBuildRoleArn" + pipeline_name_suffix)

        project = codebuild.PipelineProject(
            self,
            "Build" + pipeline_name_suffix,
            build_spec=codebuild.BuildSpec.from_source_filename("buildspec.yml"),
            environment=codebuild.BuildEnvironment(
                build_image=LinuxBuildImage.from_code_build_image_id("aws/codebuild/standard:7.0")
            ),
            role=iam.Role.from_role_arn(self, "ImportedCodeBuildRole" + pipeline_name_suffix, role_arn=codebuild_role_arn),
        )

        build_action = codepipeline_actions.CodeBuildAction(
            action_name="BuildAction" + pipeline_name_suffix,
            input=source_output,
            project=project,
            outputs=[build_output],
            environment_variables={
                "CL_FRONT_DIST_ID": codebuild.BuildEnvironmentVariable(value=distribution_id),
            },
        )

        frontpipeline.add_stage(stage_name="Build" + pipeline_name_suffix, actions=[build_action])
