# Hai: Heuristic AI

## 1. Description and Demo in GIF
Heuristic enables users to ask questions in Slack/discord/teams and receive answers from all conversations within all channels. It utilizes a simple and intuitive way to search for answers and returns relevant responses quickly. With this app, you can easily access knowledge from your team and make informed decisions based on accurate information.

![Alt](assets/TrimedGIF.gif)


## 2. Architecture 🏗️

![Alt](assets/image.png)


## 3. Tech stack 🏗️

- [x] **Cohere**: Generative [model](https://docs.cohere.ai/docs/generation-card) `command-xlarge-nightly` which allow us to extract the answer to the user's query from the extracted passage. We used Cohere also to  encode user conversation (embedding vectors). We use 
- [x] **Qdrant**: The vector search engine (`1GB RAM - 0.5 vCPU - 20GB DISK`) we have used after making a [benchmark](https://github.com/qdrant/vector-db-benchmark) of {Qdrant, Milvus, Faiss}. After evaluation, Qdrant is the fastest way to search index and very easy manipulate collections (intuitively).
- [x] **Slack_bolt**: It is a Python framework that makes it easier to build Slack apps with the platform's latest features. We could have been able to distribute the slack app (via OAuth & Permissions), but due to time constrains, the app is running on our [Heuristic AI Slack server](https://join.slack.com/t/heuristicai/shared_invite/zt-1reg204at-6BlH_V5E4r18BnpZX2JByA), you can join easily and test it features.
- [x] **Ngrok**: It is a simplified API that adds connect local wep appplication to the any cloud. It forward all user query to Amazon EC2 which make the text generation 🏗️
- [x] **Amazon EC2**: Used to host the ngrok, and slack_app

### How to use

If you want to replicate and have this Alpha version of our app on your slack, that is the main step to follow: