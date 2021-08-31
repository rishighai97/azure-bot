#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

#    PORT = 3978
#    APP_ID = os.environ.get("MicrosoftAppId", "")
#    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "5df6d5dd-e983-4e3c-a739-5f8bafb368d5")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "!9ll:$J=&nJDT{dwdzOK}C%;7hyB.")
    QNA_KNOWLEDGEBASE_ID = os.environ.get("QnAKnowledgebaseId", "1093452c-4ddc-4070-b4b6-cafea227b487")
    QNA_ENDPOINT_KEY = os.environ.get("QnAEndpointKey", "db39a326-4b3e-4058-9ef8-04c23207f514")
    QNA_ENDPOINT_HOST = os.environ.get("QnAEndpointHostName", "https://chatbot-cowin-qna.azurewebsites.net/qnamaker")
    CV_SUBSCRIPTION_KEY1 = os.environ.get("CVSubscriptionKey1", "d27103a850c04079bb365dd8cfedcf53")
    CV_SUBSCRIPTION_KEY2 = os.environ.get("CVSubscriptionKey2", "4735d337d3874db4a3bcd655e73b9843")
    CV_END_POINT_KEY = os.environ.get("CVEndpointKey", "https://chatbot-cowin-computervision.cognitiveservices.azure.com/")
    BING_END_POINT = os.environ.get("BING_END_POINT", "https://api.bing.microsoft.com/v7.0/search")
    BING_KEY1 = os.environ.get("BING_KEY1", "ac85703fb7f846bc81acbd45f99c86d8")
    BING_KEY2 = os.environ.get("BING_KEY2", "f8378ea5fc2f4adcb8d90de2a711f89a")
