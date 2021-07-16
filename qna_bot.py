from botbuilder.core import TurnContext, ActivityHandler, MessageFactory
from botbuilder.ai.qna import QnAMaker, QnAMakerEndpoint
from properties import *


class QnaBot(ActivityHandler):
    def __init__(self):
        qna_endpoint = QnAMakerEndpoint(qna_maker_key, qna_maker_endpoint_key, qna_maker_endpoint)
        self.qna_maker = QnAMaker(qna_endpoint)

    async def on_message_activity(self, turn_context: TurnContext):
        response = await self.qna_maker.get_answers(turn_context)
        if response and len(response) > 0:
            print('Questions: {}'.format(response[0].questions))
            print('Answer: {}'.format(response[0].answer))
            await turn_context.send_activity(MessageFactory.text(response[0].answer))
        else:
            print('No response found')
            await turn_context.send_activity(MessageFactory.text('I did not understand the question'))


if __name__ == '__main__':
    print('Running qna_bot')
