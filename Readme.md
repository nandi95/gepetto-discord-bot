# Discord OpenAI Bot

This bot uses OpenAI to generate responses to messages in a Discord server. It listens for mentions of the bot and generates responses using OpenAI's GPT chat model. It has some special functionality to track the number of times a user has mentioned the bot recently and limit the number of OpenAI calls.

It has a couple of extra options to do common things.  Eg:
```
@Gepetto create an image of a rocket flying through space
@Gepetto can you summarised this webpage? https://www.example.com/an/article
@Gepetto 👀 <https://www.youtube.com/watch?v=123f830q9>
@Gepetto 👀 <https://www.example.com/an/article> can you give me the main insights on this as bullet points?
@Gepetto weather forecast for London today?
```
The youtube one depends on their being subtitles/transcripts attached to the video.  The summarise command is a little limited (currently hard-coded) in scope due to token limits on the text you can send to the cheaper OpenAI models.

It has a few 'timed' features too :

* Once a day read the channel history and use an image generator (via replicate) to create an image based on the chat.
* Randomly through the night post very short 'horror stories' (usually just a single sentence)
* Occassionally just interject some chat (disabled by default as it's quite annoying)

## Environment Variables

The script uses the following environment variables (* indicates required):

| Environment Variable | Purpose | Default | Example |
|---------------------|---------|---------|---------|
| * DISCORD_SERVER_ID | Discord server identification | "not_set" | "123456789012345678" |
| * DISCORD_BOT_TOKEN | Discord bot authentication | "not_set" | "your-discord-bot-token" |
| * DISCORD_BOT_CHANNEL_ID | Setting the Discord channel ID for bot interactions | "Invalid" | "123456789012345678" |
| DISCORD_BOT_DEFAULT_PROMPT | Setting the default system prompt for the bot | - | "You are a helpful AI assistant..." |
| * BOT_PROVIDER | Selecting the AI model provider to use with litellm | - | "openai" |
| * BOT_MODEL | Setting the default model for the bot | - | "o4-mini" |
| BOT_LOCATION | Bot's location setting | "dunno" | "London" |
| BOT_NAME | Setting the bot's name | "Base" | "Gepetto" |
| CHAT_IMAGE_HOUR | Setting the hour for chat image generation | 17 | "17" (5 PM) |
| FEATURE_RANDOM_CHAT | Enabling/disabling random chat feature | False | "true" |
| FEATURE_HORROR_CHAT | Enabling/disabling horror chat feature | False | "true" |
| CHAT_IMAGE_ENABLED | Enabling/disabling chat image generation | False | "true" |
| SENTRY_AUTH_TOKEN | Sentry API authentication | - | "your-sentry-auth-token" |
| BOT_OMNILISTENS | Enabling/disabling omnilistens feature | "false" | "true" |
| MET_OFFICE_API_KEY | Weather API authentication | - | "your-met-office-api-key" |
| DISCORD_BOT_BIRTHDAYS | Storing birthday information about users (user-id:day/month) | - | "123456789:25/12,987654321:01/01" |
| ANYSCALE_API_KEY | Anyscale API authentication | - | "your-anyscale-api-key" |
| ANYSCALE_BASE_URL | Anyscale API base URL | - | "https://api.any scale.com/v1/" |
| OPENAI_API_KEY | OpenAI API authentication | - | "your-openai-api-key" |
| OPENROUTER_API_KEY | OpenRouter API authentication | - | "your-openrouter-api-key" |
| ANTHROPIC_API_KEY | Anthropic API authentication | - | "your-anthropic-api-key" |
| REPLICATE_API_KEY | Replicate API authentication (for image generation) | - | "your-replicate-api-key" |
| USER_LOCATIONS | Setting user locations for image generation | "the UK towns of Bath and Manchester" | "London, Manchester, Edinburgh" |
| USER_DESCRIPTIONS | Setting user descriptions for image generation | "UK-based Caucasian adult male IT workers" | "professional software developers" |

## Running the Script

To run the bot:

1. Install the required Python dependencies by running `pip install -r requirements.txt`.
2. Set your environment variables. These can be set in your shell, or stored in a `.env` file at the root of your project.
3. Run `python main.py` in the root of your project to start the bot.

## Docker Deployment

A `Dockerfile` is included in this repository. This allows you to easily build and run your bot inside a Docker container.  Please see the `run.sh` script for an example of building and running the container.
