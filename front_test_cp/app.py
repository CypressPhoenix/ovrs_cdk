from aws_cdk import App
from front_test_cp.front_test_cp_stack import FrontTest
import os
from dotenv import load_dotenv
load_dotenv()

region = os.environ.get("REGION_HOME")

app = App()
FrontTest(app, "FrontTest", env={'region': region})
app.synth()