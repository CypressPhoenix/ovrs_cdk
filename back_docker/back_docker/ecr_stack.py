from aws_cdk import (
    aws_ecr,
    Stack,

)
from constructs import Construct
import os
from dotenv import load_dotenv

load_dotenv()


class FrontMain(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        environment = os.environ.get("ENV")

        if environment == "dev":
            name_suffix = "dev"
        elif environment == "main":
            name_suffix = "main"
        elif environment == "test":
            name_suffix = "test"
        else:
            raise ValueError("Unknown environment: {}".format(environment))


        repository = aws_ecr.Repository(
            self, "Repository"+name_suffix,
            image_scan_on_push=True,
            repository_name="ECR"+name_suffix,
            )