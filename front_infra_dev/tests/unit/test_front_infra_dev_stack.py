import aws_cdk as core
import aws_cdk.assertions as assertions

from front_infra_dev.front_infra_dev_stack import FrontInfraDevStack

# example tests. To run these tests, uncomment this file along with the example
# resource in front_infra_dev/front_infra_dev_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = FrontInfraDevStack(app, "front-infra-dev")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
