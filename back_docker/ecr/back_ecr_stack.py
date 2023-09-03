from aws_cdk import (
    aws_ecr,
    Stack,
    CfnOutput,
    aws_iam


)
from constructs import Construct
import os
from dotenv import load_dotenv
from utils.environment import get_name_suffix

load_dotenv()


class ECR(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        name_suffix = get_name_suffix()

        # Создаем роль IAM


        # Добавляем политики к роли
        ecr_policy = aws_iam.PolicyDocument(
            statements=[
                aws_iam.PolicyStatement(
                    actions=[
                        "ecr:GetAuthorizationToken",
                        "ecr:BatchGetImage",
                        "ecr:GetDownloadUrlForLayer",
                        "ecr:PutImage",
                        "ecr:TagImage"
                    ],
                    effect=aws_iam.Effect.ALLOW,
                    resources=["*"]
                )
            ]
        )
        ecr_role = aws_iam.Role(
            self,
            "ECRRole" + name_suffix,
            assumed_by=aws_iam.ServicePrincipal("codebuild.amazonaws.com"),
            inline_policies={
                "CodeBuildPolicy"+name_suffix: ecr_policy,
            },

        )

        # Создаем репозиторий ECR
        docker_back_repository = aws_ecr.Repository(
            self,
            "DockerBackRepository" + name_suffix,
            repository_name="ecr" + name_suffix,
        )
        docker_back_repository.grant_push(ecr_role)

        docker_back_repository.add_lifecycle_rule(max_image_count=3)

        # Экспортируем URL образа с тегом "latest" как выход из стека
        CfnOutput(self, "ECRRepositoryUriOutputTag", value=docker_back_repository.repository_uri_for_tag("latest"), export_name="ECRRepositoryUriTag" + name_suffix)
        CfnOutput(self, "ECRRepositoryUriOutput", value=docker_back_repository.repository_uri,
                  export_name="ECRRepositoryUri" + name_suffix)