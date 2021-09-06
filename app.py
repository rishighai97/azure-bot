# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import sys
import traceback
from datetime import datetime
from http import HTTPStatus

from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    TurnContext,
    BotFrameworkAdapter,
)

from flask import Flask, request, Response
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext, ConversationState, \
    MemoryStorage
from botbuilder.schema import Activity, ActivityTypes

from bots import QnABot
from config import DefaultConfig
import logging
import asyncio

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True
loop = asyncio.get_event_loop()

CONFIG = DefaultConfig()

# Create the Bot
BOT = QnABot(CONFIG)

SETTINGS = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)


# Listen for incoming requests on /api/messages
@app.route("/api/messages", methods=["POST"])
def messages():
    print("Got a request for messages")
    # Main bot message handler.
    if "application/json" in request.headers["Content-Type"]:
        body = request.json
    else:
        return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    activity = Activity().deserialize(body)
    auth_header = request.headers["Authorization"] if "Authorization" in request.headers else ""

    async def call_fun(turncontext):
        await BOT.on_turn(turncontext)

    task = loop.create_task(
        ADAPTER.process_activity(activity, auth_header, call_fun)
    )

    loop.run_until_complete(task)
    return 'OK'


# Catch-all for errors.
async def on_error(context: TurnContext, error: Exception):
    # This check writes out errors to console log .vs. app insights.
    # NOTE: In production environment, you should consider logging this to Azure
    #       application insights.
    print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()

    # Send a message to the user
    await context.send_activity("The bot encountered an error or bug.")
    await context.send_activity(
        "To continue to run this bot, please fix the bot source code."
    )
    # Send a trace activity if we're talking to the Bot Framework Emulator
    if context.activity.channel_id == "emulator":
        # Create a trace activity that contains the error object
        trace_activity = Activity(
            label="TurnError",
            name="on_turn_error Trace",
            timestamp=datetime.utcnow(),
            type=ActivityTypes.trace,
            value=f"{error}",
            value_type="https://www.botframework.com/schemas/error",
        )
        # Send a trace activity, which will be displayed in Bot Framework Emulator
        await context.send_activity(trace_activity)


ADAPTER.on_turn_error = on_error

if __name__ == '__main__':
    print('Running app')
    app.run("localhost", CONFIG.PORT)
