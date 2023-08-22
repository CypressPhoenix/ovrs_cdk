from aws_cdk import App
from back_docker.ecr_stack import DatabaseStackMain
import os
from dotenv import load_dotenv
load_dotenv()

region = os.environ.get("REGION_HOME")

app = App()
DatabaseStackMain(app, "DynamoDBMain", env={'region': region})
app.synth()