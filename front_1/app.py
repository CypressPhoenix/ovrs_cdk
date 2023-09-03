from aws_cdk import App
from front_infra_stack.front_infra_stack import FrontInfra
from front_iam_stack.front_iam_stack import FrontIAM
from front_codepipeline_stack.front_cp_stack import FrontCP
import os
from dotenv import load_dotenv
from utils.environment import get_name_suffix
load_dotenv()

class MyApp(App):
    def __init__(self):
        super().__init__()

        name_suffix = get_name_suffix()

        region = os.environ.get("REGION_HOME")

        FrontCP(self, "FrontCP"+name_suffix, env={'region': region})
        FrontIAM(self, "FrontIAM"+name_suffix, env={'region': region})
        FrontInfra(self, "FrontInfra"+name_suffix, env={'region': region})

app = MyApp()
app.synth()
