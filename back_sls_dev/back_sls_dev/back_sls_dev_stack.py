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


class SLSDev(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        connection_arn = os.environ.get("CONNECTION_ARN")
        git_branch = os.environ.get("GIT_BRANCH_DEV")
        git_repo_name = os.environ.get("GIT_REPO_NAME_SLS")
        git_repo_owner = os.environ.get("GIT_REPO_OWNER")
        CardsTableArnDev = Fn.import_value("CardsTableArnDev")
        ColumnsTableArnDev = Fn.import_value("ColumnsTableArnDev")
        ColumnsTableNameDev = Fn.import_value("ColumnsTableNameDev")
        CardsTableNameDev = Fn.import_value("CardsTableNameDev")

        backslsdevpipeline = codepipeline.Pipeline(self, "BackDevSLS", pipeline_name="BackDevSLS",)

        source_output = codepipeline.Artifact()
        build_output = codepipeline.Artifact()

        sls_role = iam.Role(
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

        github_source_action_dev = codepipeline_actions.CodeStarConnectionsSourceAction(
            action_name="GitHubSourceDevSLS",
            owner=git_repo_owner,
            repo=git_repo_name,
            branch=git_branch,
            connection_arn=connection_arn,
            output=source_output,
            trigger_on_push=True,
        )

        backslsdevpipeline.add_stage(stage_name="SourceDevSLS", actions=[github_source_action_dev])

        codebuild_role_arn_dev = Fn.import_value("CodeBuildRoleArnDev")

        project_dev = codebuild.PipelineProject(
            self,
            "BuildDevSLS",
            build_spec=codebuild.BuildSpec.from_source_filename("buildspec.yml"),
            environment=codebuild.BuildEnvironment(
                build_image=LinuxBuildImage.from_code_build_image_id("aws/codebuild/standard:7.0")
            ),
            role=sls_role,
        )

        build_action_dev_SLS = codepipeline_actions.CodeBuildAction(
            action_name="BuildActionDevSLS",
            input=source_output,
            project=project_dev,
            outputs=[build_output],
            environment_variables={
                "COLUMNS_TABLE_ARN": codebuild.BuildEnvironmentVariable(value=CardsTableArnDev),
                "CARDS_TABLE_ARN": codebuild.BuildEnvironmentVariable(value=ColumnsTableArnDev),
                "COLUMNS_TABLE_NAME": codebuild.BuildEnvironmentVariable(value=ColumnsTableNameDev),
                "CARDS_TABLE_NAME": codebuild.BuildEnvironmentVariable(value=CardsTableNameDev),
            },
        )

        backslsdevpipeline.add_stage(stage_name="BuildDevSLS", actions=[build_action_dev_SLS])

