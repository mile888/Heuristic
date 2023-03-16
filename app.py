import os
# Use the package we installed
from slack_bolt import App
from internal_api import Heuristic
from template_block._blocker import block_answer, block_setup

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)


# Listenning to events
@app.message("hai")
def message_hai(message, say):
    if "setup" in message["text"].lower():
        hai = Heuristic()

        block = block_setup()
        say(
            blocks=block
        )
        hai.setup()
        block = block_setup(answer="Indexing done :sunglasses:")
        say(
            blocks=block
        )

    else:
        answer = "{}".format("This is a answer to a user query")
        link = "https://heuristicai.slack.com/archives/C04UMPXL7CG/p1678860294484939"

        query = message["text"]
        block = block_answer(answer, message["user"], link)
        say(
            blocks=block
        )

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))

