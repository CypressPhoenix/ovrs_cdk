from aws_cdk import App
from front_cloudfront_stack.front_cloudfront_stack import FrontCLoudfront
from front_iam_stack.front_iam_stack import FrontIAM
from front_s3bucket_stack.front_s3_stack import FrontS3
from front_codepipeline_stack.front_cp_stack import FrontCP
import os
from dotenv import load_dotenv
load_dotenv()

class MyApp(App):
    def __init__(self):
        super().__init__()

        environment = os.environ.get("ENV")
        if environment == "dev":
            name_suffix = "dev"
        elif environment == "main":
            name_suffix = "main"
        elif environment == "test":
            name_suffix = "test"
        else:
            raise ValueError("Unknown environment: {}".format(environment))

        region = os.environ.get("REGION_HOME")

        FrontCP(self, "FrontCP"+name_suffix, env={'region': region})
        FrontS3(self, "FrontS3"+name_suffix, env={'region': region})
        FrontIAM(self, "FrontIAM"+name_suffix, env={'region': region})
        FrontCLoudfront(self, "FrontCLoudfront"+name_suffix, env={'region': region})

app = MyApp()
app.synth()
