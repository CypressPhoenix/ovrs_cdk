from aws_cdk import App
from front_infra_test.front_infra_test_stack import FrontInfraTest
import os
from dotenv import load_dotenv
load_dotenv()

region = os.environ.get("REGION_HOME")

app = App()
FrontInfraTest(app, "FrontInfraTest", env={'region': region})
app.synth()