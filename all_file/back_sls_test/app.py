from aws_cdk import App
from back_sls_test.back_sls_test_stack import SLSTest
import os
from dotenv import load_dotenv
load_dotenv()

region = os.environ.get("REGION_HOME")

app = App()
SLSTest(app, "SLSTest", env={'region': region})
app.synth()