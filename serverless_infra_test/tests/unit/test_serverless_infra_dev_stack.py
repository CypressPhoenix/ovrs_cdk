import aws_cdk as core
import aws_cdk.assertions as assertions

from serverless_infra_main.serverless_infra_main_stack import ServerlessInfraMainStack

# example tests. To run these tests, uncomment this file along with the example
# resource in serverless_infra_test/serverless_infra_test_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ServerlessInfraMainStack(app, "serverless-infra-main")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
