from aws_cdk import App
from serverless_infra_main.serverless_infra_main_stack import DatabaseStack
import os
from dotenv import load_dotenv
load_dotenv()

region = os.environ.get("REGION_HOME")

app = App()
DatabaseStack(app, "DynamoDBMain", env={'region': region})
app.synth()