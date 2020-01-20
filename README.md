[![CircleCI](https://circleci.com/gh/Apokly/python_ucb/tree/master.svg?style=svg)](https://circleci.com/gh/Apokly/python_ucb/tree/master)

# Description
A simple HTTP server that handle requests to feed a LinUCB machine learning algorithm

# Dependencies
- Python 3

# How to run it ?
```bash
pip3 install -r requirements.txt
python3 src/server.py
```
Otherwise, you can use docker to run it (see Dockerfile)

# Endpoints:
- GET /thetas : Get current thetas values
- GET /a : Get current a values
- GET /b : Get current b values
- POST /arms : Create arms (n_arms)
- POST /reward : Send reward (arm, reward, x)
- POST /tirages : Send tirages (generated random for moment)
- DELETE /arms/n : Delete arm (n)
- POST /features : Add n feature(s)
- GET /stats : Get stats
- GET /ping : Respond pong if API is running

# Example requests :

## Get current theta values :
```bash
curl -X GET \
  http://127.0.0.01:8080/thetas
```

## Get current a values :
```bash
curl -X GET \
  http://127.0.0.01:8080/a
```

## Get current b values :
```bash
curl -X GET \
  http://127.0.0.01:8080/b
```

## Pick arm :
```bash
curl -X POST \
  http://localhost:8080/tirages \
  -H 'content-type: application/x-www-form-urlencoded' \
  -d 'n=4&X=%7B%20%22a%22%3A%20%5B100%2C%207%5D%2C%20%22b%22%3A%20%5B10%2C%2044%5D%2C%20%22e%22%3A%20%5B100%2C%2091%5D%2C%20%22f%22%3A%20%5B10%2C%2092%5D%20%7D'
```

## Post reward :
```bash
curl -X POST \
  http://localhost:8080/reward \
  -H 'content-type: application/x-www-form-urlencoded' \
  -d 'arm=e&reward=100&x=0.94327796315973622&x=0.98546216493058936'
```

## Add arm :
```bash
curl -X POST \
  http://127.0.0.01:8080/arms \
  -H 'content-type: application/x-www-form-urlencoded' \
  -d 'arms=e&arms=f'
```

## Delete arm :
```bash
curl -X DELETE \
  http://localhost:8080/arms/e
```

## Add feature :
``` bash
curl -X POST \
  http://127.0.0.01:8080/features \
  -H 'content-type: application/x-www-form-urlencoded' \
  -d n=1
```

## Stats :
```bash
curl -X GET \
  http://127.0.0.01:8080/stats
```

## Ping :
```bash
curl -X GET \
  http://127.0.0.01:8080/ping
```

## Virtualenv + dependencies commands :
```bash
pip install virtualenv
virtualenv venv
source venv/bin/activate
deactivate

pip freeze > requirements.txt
pip install -r requirements.txt
```
