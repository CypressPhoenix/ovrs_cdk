from aws_cdk import App
from front_dev_cp.front_dev_cp_stack import FrontDev
import os
from dotenv import load_dotenv
load_dotenv()

region = os.environ.get("REGION_HOME")

app = App()
FrontDev(app, "FrontDev", env={'region': region})
app.synth()