docker build --no-cache -t oshhcar/reversi .
docker stop reversi
docker rm reversi
docker run -it -d --name=reversi -p 80:3000 oshhcar/reversi