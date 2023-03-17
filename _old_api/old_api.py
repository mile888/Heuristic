import os
import cohere
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
co = cohere.Client(os.environ.get("COHERE_API_TOKEN"))

logger = logging.getLogger(__name__)

# find a conversation
def find_channel_id(channel_name="general"):
    
    conversation_id = None
    try:
        # Call the conversations.list method using the WebClient
        for result in client.conversations_list():
            if conversation_id is not None:
                break
            for channel in result["channels"]:
                if channel["name"] == channel_name:
                    conversation_id = channel["id"]
                    #Print result
                    print(f"Found conversation ID: {conversation_id}")
                    break

    except SlackApiError as e:
        print(f"Error: {e}")

    return conversation_id

def retrieve_messages_from_channel(channel_id):
    # Store conversation history
    conversation_history = []
    
    try:
        # Call the conversations.history method using the WebClient
        # conversations.history returns the first 100 messages by default
        result = client.conversations_history(channel=channel_id)

        conversation_history = result["messages"]

        # Print results
        logger.info("{} messages found in {}".format(len(conversation_history), channel_id))

    except SlackApiError as e:
        logger.error("Error creating conversation: {}".format(e))
    
    return conversation_history

def find_message(channel_id, message_id):
    message = None
    try:
        # Call the conversations.history method using the WebClient
        # The client passes the token you included in initialization    
        result = client.conversations_history(
            channel=channel_id,
            inclusive=True,
            oldest=message_id,
            limit=1
        )

        message = result["messages"][0]["text"]
        # Print message text
        print(message)

    except SlackApiError as e:
        print(f"Error: {e}")

    return message

def find_thread_messages(channel_id, message_id):
    messages = []
    try:
        # Call the conversations.history method using the WebClient
        # The client passes the token you included in initialization    
        result = client.conversations_replies(
            channel=channel_id,
            ts=message_id,
            limit=200
        )

        messages = result["messages"]

    except SlackApiError as e:
        print(f"Error: {e}")

    return messages


if __name__ == "__main__":
    channels = client.conversations_list()

    print("Found {} channels".format(len(channels["channels"])))
    payload = []
    vectors = []
    idx = []

    for channel_detail in channels["channels"]:
        channel_id = channel_detail["id"]
        channel_messages = retrieve_messages_from_channel(channel_id)
        print("Found {} messages from {} channel".format(len(channel_messages), channel_detail["name"]))

        for message in channel_messages:
            
            ts = message["ts"]
            joined_child = ""

            # find all the thread messages
            thread_messages = find_thread_messages(channel_id, ts)

            # join all the threaded messages
            _threads = []

            for _tm in thread_messages:
                if "hai" in _tm["text"].lower():
                    pass
                elif "bot_id" in _tm:
                    pass
                elif "This message was deleted" in _tm["text"]:
                    pass
                elif "has joined the channel" in _tm["text"]:
                    pass
                else:
                    _threads.append( _tm["text"].replace('\n', ''))

            mess = " ".join(_threads)
            
            payload.append({
                "message_id": ts,
                "passage": mess,
                "user": message["user"],
                "url": client.chat_getPermalink(channel=channel_id, message_ts=ts)["permalink"]
            })
            vectors.append(co.embed(texts=[mess], model="multilingual-22-12").embeddings[0])
            idx.append(message["user"])
    
    print(payload[0], vectors[0], idx[0])