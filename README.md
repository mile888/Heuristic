# Hai: Heuristic AI

## 1. Description and Demo in GIF
Heuristic enables users to ask questions in Slack/discord/teams and receive answers from all conversations within all channels. It utilizes a simple and intuitive way to search for answers and returns relevant responses quickly. With this app, you can easily access knowledge from your team and make informed decisions based on accurate information.

Building demo... 🏗️ : _That means everything will be ready on time, before 11:59 PM CET_


## 2. Architecture

Designing... 🏗️


## 3. Tech stack

- [x] Cohere: Generative model `command-xlarge-nightly` which allow us to extract the answer to the user query from the extracted passage. We used Cohere also to  encode user conversation (embedding vectors). We use 
- [x] Qdrant: The vector search engine we have used after making some benchmark {Qdrant, Milvus, Faiss}. Qdrant is the fastest way to search index and very easy manipulate collection (intuitively).
- [x] Slack_bolt: It is a python framework that makes it easier to build Slack apps with the platform's latest features. We could have been able to distribute the slack app (via OAuth & Permissions), but due to time constrains, the app is running on our [Heuristic AI Slack server](https://join.slack.com/t/heuristicai/shared_invite/zt-1reg204at-6BlH_V5E4r18BnpZX2JByA), you can join easily and test it features.
- [x] Ngrok: desc 🏗️
- [x] AWS EC2: desc 🏗️

### How to use

After that the Demo is done... 🏗️