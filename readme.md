# DeepL Document Translator for Slack

This project demonstrates how to use [DeepL's document translation API](https://www.deepl.com/docs-api/translating-documents/) in [Slack](https://slack.com/). With this app, you can translate the documents uploaded in Slack just by adding a national flag reaction emoji. When the translation is done, the app uploads the generated files in the original message's thread.

If you are looking for a solution to translate chat message text in Slack, try https://github.com/seratch/deepl-for-slack out for the purpose. You can use both apps together.

## Features

This app provides two features as below.

### Document Translator in Slack Channels

When a user adds a reaction to a message with files, this app calls [DeepL's document translation API](https://www.deepl.com/docs-api/translating-documents/).
When the translation is done, this app uploads the result as a new file in the message's thread.

<img width="500" src="https://user-images.githubusercontent.com/19658/161482554-fe0828c1-4058-4cab-9b20-0c7af9bbdb6b.png">

### Usage Dashboard

Anyone in the Slack workspace can check the remaining amount of the DeepL API calls by accessing the app's Home tab.

<img width="500" src="https://user-images.githubusercontent.com/19658/161419330-a459b6ee-e19e-4ab0-b06e-6f0b3be2fb77.png">

## Prerequisites

If you don't have any of the following accounts, create your accounts first.

* [DeepL Pro (for Developers) account](https://www.deepl.com/pro/change-plan#developer)
* [Slack workspace and user account](https://slack.com/)

## Setup

All you need to do to run this app are DeepL API key and Slack app's tokens. Follow the below steps to get the credentials.

### Create your DeepL Pro (for Developers) account

* Select "for Developers" plan at https://www.deepl.com/pro/ (be careful not to choose any other)
* Go to your [DeepL Pro Account](https://www.deepl.com/pro-account.html) page
* Save the **Authentication Key for DeepL API** value

You will use this token as `DEEPL_AUTH_KEY` env variable later.

Also, if your app allows your end-users to translate **PDF files** too, go to [Translation Settings](https://www.deepl.com/pro-account/translationSettings) and enable the "Allow PDF files to be sent to Adobe for all your future translations" option.

Refer to the following resources for more details:

* https://www.deepl.com/docs-api/
* https://www.deepl.com/pro/change-plan#developer

### Create your Slack App

Create a new Slack app from https://api.slack.com/apps?new_app=1

```yaml
display_information:
  name: DeepL Document Translator
  description: Generates translated documents from the ones uploaded in Slack
  background_color: "#0b1f5c"
features:
  app_home:
    home_tab_enabled: true
    messages_tab_enabled: true
    messages_tab_read_only_enabled: false
  bot_user:
    display_name: DeepL Document Translator
    always_online: true
oauth_config:
  scopes:
    bot:
      - chat:write
      - channels:history
      - groups:history
      - mpim:history
      - im:history
      - files:read
      - files:write
      - reactions:read
settings:
  event_subscriptions:
    bot_events:
      - app_home_opened
      - reaction_added
  interactivity:
    is_enabled: true
  socket_mode_enabled: true
```

### Install the Slack app into your Slack workspace

Go to **Settings** > **Install App** and click the **Install to Workspace** button.
You will use this `xoxb-` prefix token as `SLACK_BOT_TOKEN` env variable later.

### Enable Socket Mode for the app

Go to **Settings** > **Basic Information** > **App-Level Tokens** and click the **Generate Tokens and Scopes** button.
Create a new App-Level token with `connections:write` scope.
You will use this `xapp-` prefix token as `SLACK_APP_TOKEN` env variable later.

### Start your bolt-python app

If you haven't installed [Poetry](https://python-poetry.org/) in your local machine, install the build tool first. Once you install the tool, run the following commands.

```bash
git clone git@github.com:seratch/deepl-document-translator-for-slack.git
cd deepl-document-translator-for-slack/

# Python 3.9+ required
poetry shell
poetry install

export DEEPL_AUTH_KEY=...
export SLACK_APP_TOKEN=xapp-1-...
export SLACK_BOT_TOKEN=xoxb-...

python app.py
```

## Deployments

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/seratch/deepl-document-translator-for-slack/tree/main)

> If you encounter "We couldn't deploy your app because the source code violates the Salesforce Acceptable Use and External-Facing Services Policy." error with the above button,
> please fork this repository and use your own URL like `https://heroku.com/deploy?template=https://github.com/{your account}/deepl-document-translator-for-slack/tree/main`.

## Related Projects

If you are looking for more functionalities, take a look at the following projects:

* https://github.com/seratch/deepl-for-slack
* https://github.com/monstar-lab-oss/deepl-for-slack-elixir

## License

The MIT License
