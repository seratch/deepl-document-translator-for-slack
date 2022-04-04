import io
import logging
import os
import time
from typing import Optional

import deepl
import requests
from deepl import DocumentHandle
from slack_bolt import App, Say, BoltContext, Ack
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

from languages import detect_lang

logging.basicConfig(level=logging.DEBUG)

app = App(token=os.environ["SLACK_BOT_TOKEN"])

translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))


@app.event("app_home_opened")
def handle_app_home_opened_events(context: BoltContext, client: WebClient):
    usage = translator.get_usage()
    character_spent_percentage = (
        round((usage.character.count / usage.character.limit) * 100, 1)
        if usage.character.limit
        else 0
    )
    character_validity = (
        ":red_circle:"
        if usage.character.limit and usage.character.valid is False
        else ":large_blue_circle:"
    )
    character_limit_exceeded = (
        ":red_circle:"
        if usage.character.limit_exceeded is True
        else ":large_blue_circle:"
    )
    document_spent_percentage = (
        round((usage.document.count / usage.document.limit) * 100, 1)
        if usage.document.limit
        else 0
    )
    document_validity = (
        ":red_circle:"
        if usage.document.limit and usage.document.valid is False
        else ":large_blue_circle:"
    )
    document_limit_exceeded = (
        ":red_circle:"
        if usage.document.limit_exceeded is True
        else ":large_blue_circle:"
    )
    client.views_publish(
        user_id=context.user_id,
        view={
            "type": "home",
            "blocks": [
                {
                    "type": "section",
                    "block_id": "header",
                    "text": {"type": "mrkdwn", "text": "*DeepL API Usage*"},
                    "accessory": {
                        "type": "button",
                        "action_id": "link-button",
                        "text": {
                            "type": "plain_text",
                            "text": "Go to DeepL Account Page",
                        },
                        "url": "https://www.deepl.com/pro-account/usage",
                        "value": "clicked",
                    },
                },
                {"type": "divider"},
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*Characters*\n"
                            f"Budget: {usage.character.limit or '-'}\n"
                            f"Spent: {usage.character.count} ({character_spent_percentage}%)\n"
                            f"Valid: {character_validity}\n"
                            f"Limit Exceeded: {character_limit_exceeded}",
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Documents*\n"
                            f"Budget: {usage.document.limit or '-'}\n"
                            f"Spent: {usage.document.count or '-'} ({document_spent_percentage}%)\n"
                            f"Valid: {document_validity}\n"
                            f"Limit Exceeded: {document_limit_exceeded}",
                        },
                    ],
                },
            ],
        },
    )


@app.action("link-button")
def handle_some_action(ack: Ack):
    ack()


@app.event("reaction_added")
def handle_reaction_added_events(
    event: dict,
    context: BoltContext,
    say: Say,
    client: WebClient,
    logger: logging.Logger,
):
    item = event.get("item", {})
    if item.get("type") != "message":
        logger.debug("Skipped non-message type item")
        return
    channel, ts = item.get("channel"), item.get("ts")
    if channel is None or ts is None:
        logger.debug("Skipped because either channel or ts is missing")
        return
    reaction_name: str = event.get("reaction")
    lang = detect_lang(reaction_name)
    if lang is None:
        logger.debug(
            f"Skipped because no lang detected from the reaction ({event.get('reaction')})"
        )
        if reaction_name.startswith("flag-"):
            say(
                thread_ts=ts,
                text=f"Hey <@{context.user_id}>, the language used in {reaction_name} is not yet supported.",
            )
        return
    replies = client.conversations_replies(
        channel=channel,
        ts=ts,
        inclusive=True,
    )
    messages = replies.get("messages")
    parent_message = messages[0]
    if parent_message.get("thread_ts") is not None and parent_message.get(
        "ts"
    ) != parent_message.get("thread_ts"):
        logger.debug(
            f"Skipped because this is a reaction to any of the thread replies ({event.get('reaction')})"
        )
        return
    if parent_message.get("files") is None:
        logger.debug("Skipped because the parent message does not any files")
        return

    thread_ts = parent_message.get("ts")

    for file in parent_message.get("files"):
        original_name = file.get("name")
        original_title = file.get("title")
        elements = original_name.split(".")
        elements[-2] = elements[-2] + "_" + lang
        translated_file_name = ".".join(elements)

        already_translated = False
        for message in replies.get("messages"):
            # Check if the translated file is already uploaded
            if (
                message.get("files") is not None
                and message.get("files")[0].get("name") == translated_file_name
            ):
                # This lang version is already published
                logger.debug(
                    f"This {lang} version of {original_name} is already available"
                )
                already_translated = True
                break
        if already_translated:
            continue

        # Download the Slack file content
        input_document = requests.get(
            url=file.get("url_private_download"),
            headers={"Authorization": f"Bearer {client.token}"},
        ).content
        # The IO object to save the result file data returned from DeepL
        output_document = io.BytesIO()

        # Calling DeepL API
        try:
            handle: Optional[DocumentHandle] = None
            try:
                handle = translator.translate_document_upload(
                    input_document,
                    target_lang=lang.upper(),
                    filename=translated_file_name,
                )
            except Exception as e:
                say(
                    thread_ts=ts,
                    text=f"Hey <@{context.user_id}>, we failed to translate the document "
                    f"into the language used in :{reaction_name}:. "
                    f"(file: {original_name}, lang: {lang}, error: ${e})",
                )
                return

            say(
                thread_ts=thread_ts,
                text=f"Hey <@{context.user_id}>, "
                f"thanks for requesting :{reaction_name}: (lang: {lang}) translation of `{original_name}`! "
                "The DeepL backend is now working on the task :man-biking: "
                "We will post a translated file once the translation is done! :bow:",
            )

            try:
                status = translator.translate_document_get_status(handle)
                while status.ok and not status.done:
                    secs = (status.seconds_remaining or 0) / 2.0 + 1.0
                    secs = max(1.0, min(secs, 60.0))
                    time.sleep(secs)
                    status = translator.translate_document_get_status(handle)

                if status.ok:
                    translator.translate_document_download(handle, output_document)
            except Exception as e:
                say(
                    thread_ts=thread_ts,
                    text=":x: Failed to translate the document "
                    f"(file: {original_name}, reaction: :{reaction_name}:, lang: {lang}, error: {e})",
                )
                return

            if not status.ok:
                say(
                    thread_ts=thread_ts,
                    # TODO: improve this message to have the error details (need to enhance the DeepL SDK)
                    text=":x: Failed to translate the document for some reason. "
                    "The common pattern is that the original document is already written in the target language. "
                    f"(file: {original_name}, reaction: :{reaction_name}:, lang: {lang})",
                )
                return

            output_document.seek(0)
            client.files_upload(
                title=f"{original_title} ({lang})",
                filename=translated_file_name,
                file=output_document,
                channels=[channel],
                thread_ts=thread_ts,
                initial_comment=f"Hey <@{context.user_id}>, thanks for waiting!"
                f"Here is :{reaction_name}: (lang: {lang}) translation of `{original_name}` :white_check_mark:",
            )
        finally:
            output_document.close()


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
