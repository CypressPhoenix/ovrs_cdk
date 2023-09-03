from codepipeline.back_docker_stack import DockerCP
from ecr.back_ecr_stack import ECR
from ecs_stack.back_ecs_stack import ECS
from s3.back_s3_stack import S3Bucket
import os
from dotenv import load_dotenv
from utils.environment import get_name_suffix
from aws_cdk import App
load_dotenv()


class MyApp(App):
    def __init__(self):
        super().__init__()

        name_suffix = get_name_suffix()
        region = os.environ.get("REGION_HOME")

        ECR(self, "DockerECR" + name_suffix, env={'region': region})
        ECS(self, "DockerECS" + name_suffix, env={'region': region})
        S3Bucket(self, "DockerS3Bucket" + name_suffix, env={'region': region})
        DockerCP(self, "DockerCP" + name_suffix, env={'region': region})


app = MyApp()
app.synth()
