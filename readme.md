# DeepL Document Translator for Slack

This project demonstrates how to use DeepL's document translation API in Slack. With this app, you can translate the documents uploaded in Slack just by adding a national flag reaction emoji. When the translation is done, the app uploads the generated files in the original message's thread.

If you are looking for a solution to translate chat message text in Slack, try https://github.com/seratch/deepl-for-slack out for the purpose. You can use both apps together.

## Features

This app provides two features as below.

### Document translation

When a user adds a reaction to a message with files, this app calls DeepL's document translation API.
When the translation is done, this app uploads the result as a new file in the message's thread

<img width="500" src="https://user-images.githubusercontent.com/19658/161419367-c1b48d85-5bf7-4199-8857-66e5649f838a.png">

### Usage Dashboard

Anyone in the Slack workspace can check the remaining usage of the DeepL APIs in the app's Home tab.

<img width="500" src="https://user-images.githubusercontent.com/19658/161419330-a459b6ee-e19e-4ab0-b06e-6f0b3be2fb77.png">

## Prerequisites

* DeepL Pro (for Developers) account
* Slack workspace and user account

## Setup

### Create your DeepL Pro (for Developers) account

* Select "for Developers" plan at https://www.deepl.com/pro/ (be careful not to choose any other)
* Go to your [DeepL Pro Account](https://www.deepl.com/pro-account.html) page
* Save the **Authentication Key for DeepL API** value

You will use this token as `DEEPL_AUTH_KEY` env variable later.

Refer to the following resources for more details:

* https://www.deepl.com/en/pro/
* https://www.deepl.com/docs-api/

### Create your Slack App

Create a new Slack app from https://api.slack.com/apps?new_app=1

```yaml
display_information:
  name: DeepL Document Translator
  description: Generates translated documents from the ones uploaded in Slack
  background_color: "#0b1f5c"
features:
  bot_user:
    display_name: DeepL Document Translator
    always_online: true
oauth_config:
  scopes:
    bot:
      - channels:history
      - chat:write
      - files:read
      - files:write
      - groups:history
      - reactions:read
      - im:write
      - im:history
settings:
  event_subscriptions:
    bot_events:
      - reaction_added
  interactivity:
    is_enabled: true
  socket_mode_enabled: true
```

## Install the Slack app into your Slack workspace

Go to **Settings** > **Install App** and click the **Install to Workspace** button.
You will use this `xoxb-` prefix token as `SLACK_BOT_TOKEN` env variable later.

## Enable Socket Mode for the app

Go to **Settings** > **Basic Information** > **App-Level Tokens** and click the **Generate Tokens and Scopes** button.
Create a new App-Level token with `connections:write` scope.
You will use this `xapp-` prefix token as `SLACK_APP_TOKEN` env variable later.

## Start your bolt-python app

```bash
poetry shell
poetry install

export DEEPL_AUTH_KEY=...
export SLACK_APP_TOKEN=xapp-1-...
export SLACK_BOT_TOKEN=xoxb-...

python app.py
```

## Related Projects

If you are looking for more functionalities, take a look at the following projects:

* https://github.com/seratch/deepl-for-slack
* https://github.com/monstar-lab-oss/deepl-for-slack-elixir

## License

The MIT License