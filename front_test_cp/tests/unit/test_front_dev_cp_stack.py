import aws_cdk as core
import aws_cdk.assertions as assertions

from front_dev_cp.front_dev_cp_stack import FrontDevCpStack

# example tests. To run these tests, uncomment this file along with the example
# resource in front_test_cp/front_test_cp_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = FrontDevCpStack(app, "front-dev-cp")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
