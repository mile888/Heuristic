import os
# Use the package we installed
from slack_bolt import App
import cohere
from _qdrant import Qdrant
from internal_api import Heuristic
from template_block._blocker import block_answer, block_setup

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)
co = cohere.Client(os.environ.get("COHERE_API_TOKEN"))

def trim(q):

    word_list = q.lower().replace("hai", "").split()
    if len(q) > 0:
        phrase = " ".join(word_list[1:]) if word_list[0] in [",", ";"] else " ".join(word_list[:])
        return phrase
    else:
        return " ".join(word_list)

# Listenning to events
@app.message("hai")
def message_hai(message, say):
    qdrant = Qdrant(
            url=os.environ.get("QDRANT_URL"), 
            prefer_grpc=True,
            api_key=os.environ.get("QDRANT_API_TOKEN"),
        )
    
    if "setup" in message["text"].lower():
        # init message
        block = block_setup()
        say(
            blocks=block
        )
        hai = Heuristic()
        hai.setup()
       
        qdrant.drop("hai")
        qdrant.create_collection("hai")
        print({
                "idx": hai._idx
            })
        print("after create collection")
        qdrant.insert(
            {
                "idx": hai._idx,
                "payloads": hai._payload,
                "vectors": hai._vectors
            }
        )
        print("after insert")
        
        block = block_setup(answer="Indexing done and Ready to Search :sunglasses:")
        say(
            blocks=block
        )

    else:

        query = trim(message["text"])

        embed = co.embed(texts=[query], model="multilingual-22-12").embeddings[0]
        results = qdrant.search_answer(embed, topk=5)
        res = [dict(r) for r in results]
        
        passages = []
        urls = []
        users = []
        for dic in res:
            passages.append(dic["payload"]["passage"])
            urls.append(dic["payload"]["url"])
            users.append(dic["payload"]["user"])
        
        
        prompt = "Generate the answer from the following context: "
        # answers = [ 
        #             co.generate(  
        #                 model='command-medium-nightly',  
        #                 prompt = prompt + trim(context),  
        #                 max_tokens=200,  
        #                 temperature=0.650) 
        #             for context in passages
        #         ]
        answer = co.generate(  
                        model='command-xlarge-nightly',  
                        prompt = prompt + trim(passages[0]),  
                        max_tokens=200,  
                        temperature=0.750) 
        print("======", answer)
        block = block_answer(answer.generations[0].text, users[0], urls[0])
        say(
            blocks=block
        )

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))

