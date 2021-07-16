from flask import Flask,request,Response
from botbuilder.core import BotFrameworkAdapter,BotFrameworkAdapterSettings,TurnContext,ConversationState,MemoryStorage
from botbuilder.schema import Activity
import asyncio
from qna_bot import QnaBot
import requests
import json
import logging

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True
loop = asyncio.get_event_loop()

botsettings = BotFrameworkAdapterSettings("","")
botadapter = BotFrameworkAdapter(botsettings)

CONMEMORY = ConversationState(MemoryStorage())
botdialog = QnaBot()


@app.route("/api/messages",methods=["POST"])
def messages():
    if "application/json" in request.headers["content-type"]:
        body = request.json
        update_user_input_with_bing_search_response(body = body,bing_search_response = get_bing_search_response(body=body))
    else:
        return Response(status = 415)

    activity = Activity().deserialize(body)


    auth_header = (request.headers["Authorization"] if "Authorization" in request.headers else "")

    async def call_fun(turncontext):
        await botdialog.on_turn(turncontext)

    task = loop.create_task(
        botadapter.process_activity(activity,auth_header,call_fun)
        )
    loop.run_until_complete(task)
    return 'OK'


def update_user_input_with_bing_search_response(body, bing_search_response):
    try:
        if bing_search_response is not None:
            body['text'] = bing_search_response
    except Exception as e:
        print()


def get_bing_search_response(body):
    try:
        text = body['text']
        key = "4e733d5c6d704e41a1c6a7c5fa7d0e80"
        endpoint = "https://api.bing.microsoft.com/v7.0/search"

        headers = {"Ocp-Apim-Subscription-Key": key}
        params = {"q": text, "textDecorations": True, "textFormat": "HTML"}

        response = requests.get(endpoint, headers=headers, params=params)
        search_results = response.json()
        bing_response = search_results['queryContext']['alteredQuery']
        print('Input from user: {}'.format(text))
        print('Bing search response: {}'.format(bing_response))

        return bing_response
    except Exception as e:
        print(e)
        return None



if __name__ == '__main__':
    print('Running app')
    app.run('localhost',3978)