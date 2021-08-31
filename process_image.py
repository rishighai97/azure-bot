from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time

from config import DefaultConfig
from PIL import Image

'''
Authenticate
Authenticates your credentials and creates a client.
'''

async def process_image_content(turn_context, data):
    config = DefaultConfig()
    subscription_key = config.CV_SUBSCRIPTION_KEY
    endpoint = config.CV_END_POINT_KEY

    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    # Call API with image and raw response (allows you to get the operation location)
    read_response = computervision_client.read_in_stream(data, raw=True)
    # Get the operation location (URL with ID as last appendage)
    read_operation_location = read_response.headers["Operation-Location"]
    # Take the ID off and use to get results
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for the retrieval of the results
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status.lower () not in ['notstarted', 'running']:
            break
        #time.sleep(10)
    output_lines = ''
    # Print results, line by line
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                output_lines = output_lines + ' ' + line.text
    turn_context.activity.text = output_lines

'''
END - Read File - local
'''