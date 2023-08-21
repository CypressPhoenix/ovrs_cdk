import aws_cdk as core
import aws_cdk.assertions as assertions

from front_main.front_main_stack import FrontMainStack

# example tests. To run these tests, uncomment this file along with the example
# resource in front_main_stack/front_main_s3_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = FrontMainStack(app, "front-main")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
