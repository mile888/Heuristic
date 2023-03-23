import os
import cohere
from slack_bolt import App
from _qdrant import Qdrant
from _heuristic import Heuristic
from utils.string_cleaner import trim
from template_block._prompt import structure
from template_block._blocker import block_answer, block_setup
import time

start = time.time()

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)
co = cohere.Client(os.environ.get("COHERE_API_TOKEN"))
print("loading key: ",time.time() - start)

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
            start = time.time()
            hai = Heuristic()
            hai.setup()
        
            qdrant.drop("hai")
            qdrant.create_collection("hai")
            print({
                    "idx": len(hai._idx),
                    "vectors": len(hai._passages)
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
            start = time.time()
            query = trim(event["text"])
            print("trim text: ",time.time() - start)

            start = time.time()
            embed = co.embed(texts=[query], model="multilingual-22-12").embeddings[0]
            print("embed: ",time.time() - start)

            start = time.time()
            results = qdrant.search_answer(embed, topk=5)
            print("search: ",time.time() - start)
            res = [dict(r) for r in results]

            start = time.time()
            passage = res[0]["payload"]["passage"]
            url = res[0]["payload"]["url"]
            user = res[0]["payload"]["user"]
            print("Take the first elt: ",time.time() - start)
            
            # prompt = "Generate the answer from the following context: "
            prompt = structure(context=passage, query=query)

            start = time.time()
            answer = co.generate(  
                            model='command-xlarge-nightly',  
                            prompt = prompt,  
                            max_tokens=60,  
                            temperature=0.65)
            print("generate: ",time.time() - start)
            answer = answer.generations[0].text
            print("======", answer)
            block = block_answer(answer, user, url)
            say(
                blocks=block
            )
    else:
        hai = Heuristic()
        
        

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))

