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


class SLSTest(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        connection_arn = os.environ.get("CONNECTION_ARN")
        git_branch = os.environ.get("GIT_BRANCH_TEST")
        git_repo_name = os.environ.get("GIT_REPO_NAME_SLS")
        git_repo_owner = os.environ.get("GIT_REPO_OWNER")
        CardsTableArnMain = Fn.import_value("CardsTableArnMain")
        ColumnsTableArnMain = Fn.import_value("ColumnsTableArnMain")

        backslstestpipeline = codepipeline.Pipeline(self, "BackTestSLS", pipeline_name="BackTestSLS",)

        source_output = codepipeline.Artifact()
        build_output = codepipeline.Artifact()

        sls_role_test = iam.Role(
            self,
            "CodeBuildRole",
            assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonAPIGatewayInvokeFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AWSLambda_FullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"),
            ],
        )

        github_source_action_test = codepipeline_actions.CodeStarConnectionsSourceAction(
            action_name="GitHubSourceTestSLS",
            owner=git_repo_owner,
            repo=git_repo_name,
            branch=git_branch,
            connection_arn=connection_arn,
            output=source_output,
            trigger_on_push=True,
        )

        backslstestpipeline.add_stage(stage_name="SourceTestSLS", actions=[github_source_action_test])

        codebuild_role_arn_main = Fn.import_value("CodeBuildRoleArnMain")

        project_test = codebuild.PipelineProject(
            self,
            "BuildTestSLS",
            build_spec=codebuild.BuildSpec.from_source_filename("buildspec.yml"),
            environment=codebuild.BuildEnvironment(
                build_image=LinuxBuildImage.from_code_build_image_id("aws/codebuild/standard:7.0")
            ),
            role=sls_role_test,
        )

        build_action_test_SLS = codepipeline_actions.CodeBuildAction(
            action_name="BuildActionTestSLS",
            input=source_output,
            project=project_test,
            outputs=[build_output],
            environment_variables={
                "COLUMNS_TABLE_ARN": codebuild.BuildEnvironmentVariable(value=CardsTableArnMain),
                "CARDS_TABLE_ARN": codebuild.BuildEnvironmentVariable(value=ColumnsTableArnMain),
            },
        )

        backslstestpipeline.add_stage(stage_name="BuildTestSLS", actions=[build_action_test_SLS])

