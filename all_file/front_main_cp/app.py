from aws_cdk import App
from front_main_cp.fornt_main_cp_stack import FrontMain
import os
from dotenv import load_dotenv
load_dotenv()

region = os.environ.get("REGION_HOME")

app = App()
FrontMain(app, "FrontMain", env={'region': region})
app.synth()