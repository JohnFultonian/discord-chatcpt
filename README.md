### Discord ChatGPT Assistant Bot
This is designed to be a simple way to connect your discord server to ChatGPT using the OpenAI API. You can provide a system prompt to tailor the knowledge and functionality of the chat bot to be more server specific (ie, feed it your rules/faq/common questions)

#### Capabilities
 - React to any message with '?' to have it sent to the bot
 - Bot will send the message to ChatGPT and then reply
 - Follow up replies will also be sent to the bot which will maintain the conversation thread

#### Setup
 - Create a `secrets.json` file which will contain your discord bot token and OpenAI access token. Example below:

 ```

{
  "bot_token": "<discord bot token>",
  "openai_token": "<openai API token>"
}

 ```
  - Create a `system-prompt` file, any text in this file will be prepended to messages sent to ChatGPT to prime it with server specific knowledge/instructions. Example below:

```
You are a helpful discord bot for the xyz discord server.

Server rules:
...

Server FAQ:
...
```

#### Running locally
Execute the following commands in the repo directory
 - `python3 -m venv venv`
 - `source venv/bin/activate`
 - `pip3 install -r requirements.txt`
 - `python3 bot.py`
