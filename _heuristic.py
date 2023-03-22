
import os, time
import cohere
import logging
from slack_sdk import WebClient
from utils.string_cleaner import trim
from slack_sdk.errors import SlackApiError

# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.

co = cohere.Client(os.environ.get("COHERE_API_TOKEN"))

logger = logging.getLogger(__name__)
    

class Heuristic(WebClient):
    def __init__(self):
        super().__init__(token=os.environ.get("SLACK_BOT_TOKEN"))
        self._channels = []
        self._payload = []
        self._vectors = []
        self._idx = []
        
    def set_channels(self):
        self._channels = self.conversations_list()

    def retrieve_messages(self, channel_id="general"):
        # Store conversation history
        conversation_history = []
        
        try:
            # Call the conversations.history method using the WebClient
            # conversations.history returns the first 100 messages by default
            result = self.conversations_history(channel=channel_id)

            conversation_history = result["messages"]

            # Print results
            logger.info("{} messages found in {}".format(len(conversation_history), channel_id))

        except SlackApiError as e:
            logger.error("Error creating conversation: {}".format(e))
        
        return conversation_history

    def find_threaded_messages(self, channel_id, message_id):
        messages = []
        try:
            # Call the conversations.history method using the WebClient
            # The client passes the token you included in initialization    
            result = self.conversations_replies(
                channel=channel_id,
                ts=message_id,
                limit=200
            )

            messages = result["messages"]

        except SlackApiError as e:
            print(f"Error: {e}")

        return messages
    
    def setup(self):
        self.set_channels()
        print("Found -{}- channels".format(len(self._channels["channels"])))
        indexer_counter = 1

        for channel_detail in self._channels["channels"]:
            channel_id = channel_detail["id"]
            start  = time.time()
            channel_messages = self.retrieve_messages(channel_id)
            
            print("Found {} messages from <{}> channel in {}".format(len(channel_messages), channel_detail["name"], time.time() - start))

            for message in channel_messages:
                ts = message["ts"]

                # find all threaded messages
                thread_messages = self.find_threaded_messages(channel_id, ts)

                # join all the threaded messages pass useless message
                _threads = []

                for _tm in thread_messages:
                    if "hai" in _tm["text"].lower():
                        pass
                    elif "bot_id" in _tm:
                        pass
                    elif "this message was deleted" in _tm["text"].lower():
                        pass
                    elif "has joined the channel" in _tm["text"].lower():
                        pass
                    else:
                        _threads.append( trim(_tm["text"]))

                joined_child_with_parent = " ".join(_threads)
                self._payload.append({
                    "message_id": ts,
                    "passage": joined_child_with_parent,
                    "user": message["user"],
                    "url": self.chat_getPermalink(channel=channel_id, message_ts=ts)["permalink"]
                })
                self._vectors.append(
                    co.embed(texts=[joined_child_with_parent], model="multilingual-22-12").embeddings[0]
                )
                self._idx.append(indexer_counter)
                indexer_counter += 1


if __name__ == "__main__":
    hai = Heuristic()
    hai.setup()

    random_index = 5
    # print(hai._payload[random_index], hai._vectors[random_index], hai._idx[random_index])
