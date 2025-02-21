# gf-arangodb-hackathon
proof of concept and our project are there !

## run arangodb container
[docker image](https://hub.docker.com/_/arangodb)
```shell
docker run -d -p 8529:8529 -e ARANGO_ROOT_PASSWORD=somepassword --name some-arangodb arangodb
```
