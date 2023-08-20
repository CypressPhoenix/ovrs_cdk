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


class FrontTest(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        connection_arn = os.environ.get("CONNECTION_ARN")
        git_branch = os.environ.get("GIT_BRANCH_TEST_FRONT")
        git_repo_name = os.environ.get("GIT_REPO_NAME")
        git_repo_owner = os.environ.get("GIT_REPO_OWNER")
        distribution_id = Fn.import_value("DistributionIDTest")
        s3_bucket_name = Fn.import_value("BucketNameTest")

        fronttestpipeline = codepipeline.Pipeline(self, "FrontTest", pipeline_name="FronTest",)

        source_output = codepipeline.Artifact()
        build_output = codepipeline.Artifact()

        github_source_action_Test = codepipeline_actions.CodeStarConnectionsSourceAction(
            action_name="GitHubSourceTest",
            owner=git_repo_owner,
            repo=git_repo_name,
            branch=git_branch,
            connection_arn=connection_arn,
            output=source_output,
            trigger_on_push=True,
        )

        fronttestpipeline.add_stage(stage_name="SourceTest", actions=[github_source_action_Test])

        codebuild_role_arn_test = Fn.import_value("CodeBuildRoleArnTest")

        project_test = codebuild.PipelineProject(
            self,
            "BuildTest",
            build_spec=codebuild.BuildSpec.from_source_filename("buildspec.yml"),
            environment=codebuild.BuildEnvironment(
                build_image=LinuxBuildImage.from_code_build_image_id("aws/codebuild/standard:7.0")
            ),
            role=iam.Role.from_role_arn(self, "ImportedCodeBuildRole", role_arn=codebuild_role_arn_test),
        )

        build_action_test = codepipeline_actions.CodeBuildAction(
            action_name="BuildActionTest",
            input=source_output,
            project=project_test,
            outputs=[build_output],
            environment_variables={
                "CL_FRONT_DIST_ID": codebuild.BuildEnvironmentVariable(value=distribution_id),
                "S3_Content_Bucket": codebuild.BuildEnvironmentVariable(value=s3_bucket_name)
            },
        )

        fronttestpipeline.add_stage(stage_name="BuildTest", actions=[build_action_test])
