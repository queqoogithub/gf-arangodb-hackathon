# 🥑 gf-arangodb-hackathon
proof of concept and our project are there !

## Where are we? 🚀
[ ] choose a dataset: select topic (idea) and clearify real world problems will be solved 
[ ] **convert / load dataset into NetworkX**
[ ] **persist the NetworkX data to a graph within ArangoDB**
[ ] **build an Agentic App on top of graph that processes Natural Language queries**
[ ] summarize and send our project

## run arangodb container
pull this image -> [docker image](https://hub.docker.com/_/arangodb)
```shell
docker run -d -p 8529:8529 -e ARANGO_ROOT_PASSWORD=somepassword --name some-arangodb arangodb
```
