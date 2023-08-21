from aws_cdk import App
from serverless_infra_test.serverless_infra_test_stack import DatabaseStackTest
import os
from dotenv import load_dotenv
load_dotenv()

region = os.environ.get("REGION_HOME")

app = App()
DatabaseStackTest(app, "DynamoDBTest", env={'region': region})
app.synth()