# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.ai.qna import QnAMaker, QnAMakerEndpoint
from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount, Attachment

from config import DefaultConfig
import urllib.parse
import urllib.request
import base64
import json
import bots.process_image as process_image
from io import BytesIO
import requests


class QnABot(ActivityHandler):
    def __init__(self, config: DefaultConfig):
        self.qna_maker = QnAMaker(
            QnAMakerEndpoint(
                knowledge_base_id=config.QNA_KNOWLEDGEBASE_ID,
                endpoint_key=config.QNA_ENDPOINT_KEY,
                host=config.QNA_ENDPOINT_HOST,
            )
        )

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    "Hey, welcome to the Covid Chatbot.\n\n"
                    "How may I help you?"
                )

    async def on_message_activity(self, turn_context: TurnContext):
        # Check if there are attachments
        if turn_context.activity.attachments and len(turn_context.activity.attachments) > 0:
            await self._handle_incoming_attachment(turn_context)
            
        # Split the questions based on ';'
        questions_array = await self.split_and_separate_questions(turn_context)
        for question in questions_array:
            # Bing correction method
            if question.strip()=='':
                continue
            turn_context.activity.text = question
            await self._get_and_update_bing_search_response(turn_context)
            # The actual call to the QnA Maker service.
            response = await self.qna_maker.get_answers(turn_context)
            if response and len(response) > 0:
                input_type = "Showing result for -> " if question == turn_context.activity.text else "Did you mean -> "
                await turn_context.send_activity(input_type + turn_context.activity.text + "\n\n Result -> " + str(MessageFactory.text(response[0].answer).text))
            else:
                await turn_context.send_activity("I did not understand the question")

    async def split_and_separate_questions(self, turn_context):
        text = turn_context.activity.text
        print("Questions: ",text)
        text_array = text.split(';')
        return text_array

    async def _get_and_update_bing_search_response(self, turn_context):
        try:
            config = DefaultConfig()
            bing_response = turn_context.activity.text
            
            headers = {"Ocp-Apim-Subscription-Key": config.BING_KEY1}
            params = {"q": bing_response, "textDecorations": True, "textFormat": "HTML"}
            response = requests.get(config.BING_END_POINT, headers=headers, params=params)
            search_results = response.json()
            if 'alteredQuery' in search_results['queryContext']:
                bing_response = search_results['queryContext']['alteredQuery']
            if bing_response is not None:
                turn_context.activity.text = bing_response
        except Exception as e:
            print(e)
            return None

    async def _handle_incoming_attachment(self, turn_context: TurnContext):
        # Handle attachments uploaded by users. The bot receives an Attachment in an Activity.
        for attachment in turn_context.activity.attachments:
            return await self._download_attachment_and_process(attachment, turn_context)
            
    async def _download_attachment_and_process(self, attachment: Attachment, turn_context : TurnContext) -> dict:
        # Retrieve the attachment via the attachment's contentUrl.
        try:
            response = urllib.request.urlopen(attachment.content_url)
            headers = response.info()
            print("Attachment headers: ",headers)
            # If user uploads JSON file, this prevents it from being written as
            # "{"type":"Buffer","data":[123,13,10,32,32,34,108..."
            if headers["content-type"] == "application/json":
                data = bytes(json.load(response)["data"])
            else:
                data = response.read()
            output = process_image.process_image_content(turn_context, BytesIO(data))
            await output
        except Exception as exception:
            print(exception)
            return {}
