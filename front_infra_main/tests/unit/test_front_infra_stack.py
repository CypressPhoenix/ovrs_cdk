import aws_cdk as core
import aws_cdk.assertions as assertions

from front_infra_main.front_infra_stack import FrontInfraStack

# example tests. To run these tests, uncomment this file along with the example
# resource in front_infra_main/front_infra_main_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = FrontInfraStack(app, "front-infra")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
