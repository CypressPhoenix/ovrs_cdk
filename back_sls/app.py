from aws_cdk import App
from back_sls_cp.back_sls_cp_stack import SLSCodepipeline
from serverless_infra.serverless_infra_stack import DatabaseStack
import os
from dotenv import load_dotenv
from utils.environment import get_name_suffix
load_dotenv()

class MyApp(App):
    def __init__(self):
        super().__init__()

        name_suffix = get_name_suffix()

        region = os.environ.get("REGION_HOME")

        SLSCodepipeline(self, "SLSCP"+name_suffix, env={'region': region})
        DatabaseStack(self, "DatabaseStack"+name_suffix, env={'region': region})

app = MyApp()
app.synth()
