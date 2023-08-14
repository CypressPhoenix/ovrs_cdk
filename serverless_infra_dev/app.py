from aws_cdk import App
from serverless_infra_dev.serverless_infra_dev_stack import DatabaseStackDev
import os
from dotenv import load_dotenv
load_dotenv()

region = os.environ.get("REGION_HOME")

app = App()
DatabaseStackDev(app, "DynamoDBDev", env={'region': region})
app.synth()