from aws_cdk import App
from back_docker_main.back_docker_main_stack import DockerMain
import os
from dotenv import load_dotenv
load_dotenv()

region = os.environ.get("REGION_HOME")

app = App()
DockerMain(app, "DockerMain", env={'region': region})
app.synth()