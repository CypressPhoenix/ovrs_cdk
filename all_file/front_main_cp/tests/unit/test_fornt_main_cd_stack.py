import aws_cdk as core
import aws_cdk.assertions as assertions

from fornt_main_cp.fornt_main_cp_stack import ForntMainCdStack

# example tests. To run these tests, uncomment this file along with the example
# resource in front_main_cp/fornt_main_cp_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ForntMainCdStack(app, "front_main_cp")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
