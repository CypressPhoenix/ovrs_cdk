from aws_cdk import (
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codebuild as codebuild,
    Stack,
    Fn
)
from utils.environment import get_name_suffix
from constructs import Construct
import os
from dotenv import load_dotenv
from aws_cdk.aws_codebuild import LinuxBuildImage
import aws_cdk.aws_iam as iam

load_dotenv()


class SLSMain(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        name_suffix = get_name_suffix()

        connection_arn = os.environ.get("CONNECTION_ARN")
        git_repo_name = os.environ.get("GIT_REPO_NAME_SLS")
        git_repo_owner = os.environ.get("GIT_REPO_OWNER")
        CardsTableArn = Fn.import_value("CardsTableArn"+name_suffix)
        ColumnsTableArn = Fn.import_value("ColumnsTableArn"+name_suffix)
        ColumnsTableName = Fn.import_value("ColumnsTableName"+name_suffix)
        CardsTableName = Fn.import_value("CardsTableName"+name_suffix)

        backslspipeline = codepipeline.Pipeline(self, "BackSLS"+name_suffix, pipeline_name="BackSLS"+name_suffix,)

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

        github_source_action_main = codepipeline_actions.CodeStarConnectionsSourceAction(
            action_name="GitHubSourceSLS"+name_suffix,
            owner=git_repo_owner,
            repo=git_repo_name,
            branch=name_suffix,
            connection_arn=connection_arn,
            output=source_output,
            trigger_on_push=True,
        )

        backslspipeline.add_stage(stage_name="SourceSLS", actions=[github_source_action_main])

        codebuild_role_arn = Fn.import_value("CodeBuildRoleArn"+name_suffix)

        project_main = codebuild.PipelineProject(
            self,
            "BuildSLS"+name_suffix,
            build_spec=codebuild.BuildSpec.from_source_filename("buildspec.yml"),
            environment=codebuild.BuildEnvironment(
                build_image=LinuxBuildImage.from_code_build_image_id("aws/codebuild/standard:7.0")
            ),
            role=sls_role,
        )

        build_action_SLS = codepipeline_actions.CodeBuildAction(
            action_name="BuildActionSLS"+name_suffix,
            input=source_output,
            project=project_main,
            outputs=[build_output],
            environment_variables={
                "COLUMNS_TABLE_ARN": codebuild.BuildEnvironmentVariable(value=CardsTableArn),
                "CARDS_TABLE_ARN": codebuild.BuildEnvironmentVariable(value=ColumnsTableArn),
                "COLUMNS_TABLE_NAME": codebuild.BuildEnvironmentVariable(value=ColumnsTableName),
                "CARDS_TABLE_NAME": codebuild.BuildEnvironmentVariable(value=CardsTableName),

            },
        )

        backslspipeline.add_stage(stage_name="BuildSLS"+name_suffix, actions=[build_action_SLS])

