import os
import cohere
from slack_bolt import App
from _qdrant import Qdrant
from _heuristic import Heuristic
from utils.string_cleaner import trim
from template_block._prompt import structure
from template_block._blocker import block_answer, block_setup

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)
co = cohere.Client(os.environ.get("COHERE_API_TOKEN"))


# Listenning to events
@app.event("message")
def event_hai(event, say):
    qdrant = Qdrant(
            url=os.environ.get("QDRANT_URL"), 
            prefer_grpc=True,
            api_key=os.environ.get("QDRANT_API_TOKEN"),
        )
    print(event["text"].lower())
    if "hai" in event["text"].lower():

        if "setup" in event["text"].lower():
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
            qdrant.insert_batch(
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

            query = trim(event["text"])

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
            
            
            # prompt = "Generate the answer from the following context: "
            prompt = structure(context=passages[0], query=query)
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
                            prompt = prompt,  
                            max_tokens=400,  
                            temperature=0.87)
            answer = answer.generations[0].text
            print("======", answer)
            block = block_answer(answer, users[0], urls[0])
            say(
                blocks=block
            )
    else:
        hai = Heuristic()
        
        

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))

