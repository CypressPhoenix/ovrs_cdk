from aws_cdk import App
from back_sls_dev.back_sls_dev_stack import SLSDev
import os
from dotenv import load_dotenv
load_dotenv()

region = os.environ.get("REGION_HOME")

app = App()
SLSDev(app, "SLSDev", env={'region': region})
app.synth()