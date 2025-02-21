# 🥑 gf-arangodb-hackathon
Proof of Concept and our project are available here!

## Where are we? 🚀
- [ ] **Choose a Dataset**: Select a topic (idea) and clarify the real-world problems that will be solved.
- [ ] **Convert / Load Dataset into NetworkX**
- [ ] **Persist the NetworkX Data to a Graph within ArangoDB**
- [ ] **Build an Agentic App on Top of the Graph that Processes Natural Language Queries**
- [ ] **Summarize and Submit Our Project**

## Run ArangoDB Container
Pull this image -> [Docker Image](https://hub.docker.com/_/arangodb)

```shell
docker run -d -p 8529:8529 -e ARANGO_ROOT_PASSWORD=somepassword --name some-arangodb arangodb
