from aws_cdk import App
from back_sls.back_sls_main.back_sls_main_stack import SLSMain
import os
from dotenv import load_dotenv
load_dotenv()

region = os.environ.get("REGION_HOME")

app = App()
SLSMain(app, "SLSMain", env={'region': region})
app.synth()