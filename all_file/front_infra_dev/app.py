from aws_cdk import App
from front_infra_dev.front_infra_dev_stack import FrontInfraDev
import os
from dotenv import load_dotenv
load_dotenv()

region = os.environ.get("REGION_HOME")

app = App()
FrontInfraDev(app, "FrontInfraDev", env={'region': region})
app.synth()