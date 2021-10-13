#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """
#    PORT = 3978
#     APP_ID = os.environ.get("MicrosoftAppId", "")
#     APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")

    CONTENT_TYPE_TEAMS_ATTACHMENT = "application/vnd.microsoft.teams.file.download.info"
    CONTENT_TYPE_JSON = "application/json"

    PORT = 3978

    APP_ID = os.environ.get("MicrosoftAppId", "54b403f1-14fb-4eb7-a2e9-fdd8a2b2a81e")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "nPD7Q~B2XKF8-V9Ff6p.WFME51~7~8GpdleT9")

    QNA_KNOWLEDGEBASE_ID = os.environ.get("QnAKnowledgebaseId", "f282215e-315a-4805-b2e8-aeac7a06df88")
    QNA_ENDPOINT_KEY = os.environ.get("QnAEndpointKey", "903d27df-6ca6-4ce9-b9cd-d157036848b8")
    QNA_ENDPOINT_HOST = os.environ.get("QnAEndpointHostName", "https://chatbot-chapter-qna.azurewebsites.net/qnamaker")

    CV_SUBSCRIPTION_KEY1 = os.environ.get("CVSubscriptionKey1", "cd55e74812094253bd51e3156654a60c")
    CV_SUBSCRIPTION_KEY2 = os.environ.get("CVSubscriptionKey2", "5c4e8d21a2fd4f5a8efded78f00f6616")
    CV_END_POINT_KEY = os.environ.get("CVEndpointKey", "https://chatbot-cowin-cv.cognitiveservices.azure.com/")

    BING_END_POINT = os.environ.get("BING_END_POINT", "https://api.bing.microsoft.com/v7.0/search")
    BING_KEY1 = os.environ.get("BING_KEY1", "ab93c8b7e8f2407da751a2306e61a354")
    BING_KEY2 = os.environ.get("BING_KEY2", "84a44c62964149f59ce48f3be84fb11f")
