from aws_cdk import App
from codepipeline.back_docker_stack import DockerCP
from ecr.back_ecr_stack import ECR
from ecs.back_ecs_stack import ECS
from s3.back_s3_stack import S3Bucket
import os
from dotenv import load_dotenv
load_dotenv()

class MyApp(App):
    def __init__(self):
        super().__init__()

        environment = os.environ.get("ENV")
        if environment == "dev":
            name_suffix = "dev"
        elif environment == "main":
            name_suffix = "main"
        elif environment == "test":
            name_suffix = "test"
        else:
            raise ValueError("Unknown environment: {}".format(environment))

        region = os.environ.get("REGION_HOME")

        # Создание стеков
        docker_cp_stack = DockerCP(self, "DockerCP"+name_suffix, env={'region': region})
        ecr_stack = ECR(self, "DockerECR"+name_suffix, env={'region': region})
        ecs_stack = ECS(self, "DockerECS"+name_suffix, env={'region': region})
        s3_stack = S3Bucket(self, "DockerS3Bucket"+name_suffix, env={'region': region})

        # Установка зависимостей между стеками
#       ecr_stack.add_dependency(docker_stack)  # ECR зависит от DockerCP
#        ecs_stack.add_dependency(ecr_stack)      # ECS зависит от ECR

app = MyApp()
app.synth()
