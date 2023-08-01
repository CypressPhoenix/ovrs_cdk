from aws_cdk import App
from front_infra_main.front_infra_main_stack import FrontInfraMain
import os
from dotenv import load_dotenv
load_dotenv()

region = os.environ.get("REGION_HOME")

app = App()
FrontInfraMain(app, "FrontInfraMain", env={'region': region})
app.synth()