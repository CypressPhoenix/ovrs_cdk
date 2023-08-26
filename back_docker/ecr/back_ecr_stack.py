from aws_cdk import (
    aws_ecr,
    Stack,
    CfnOutput

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

        docker_back_repository = aws_ecr.Repository(
            self,
            "DockerBackRepository" + name_suffix,
            image_scan_on_push=True,
            repository_name="ecr" + name_suffix,
        )

        # Экспортируем URL образа с тегом "latest" как выход из стека
        CfnOutput(self, "ECRRepositoryUriOutput", value=docker_back_repository.repository_uri_for_tag("latest"), export_name="ECRRepositoryUri" + name_suffix)