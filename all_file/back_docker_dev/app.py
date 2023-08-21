from aws_cdk import App
from back_docker_dev.back_docker_dev_stack import DockerDev
import os
from dotenv import load_dotenv
load_dotenv()

region = os.environ.get("REGION_HOME")

app = App()
DockerDev(app, "DockerDev", env={'region': region})
app.synth()