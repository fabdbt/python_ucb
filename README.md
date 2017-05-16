# Description
A simple HTTP server that handle requests to feed a LinUCB machine learning algorithm

# Dependencies
- Python 3

# How to run it ?
```bash
python3 src/server.py
```
Otherwise, you can use docker to run it (see Dockerfile)

# Endpoints:
- GET /thetas : Get current thetas values
- POST /arms : Create arms (n_arms)
- POST /reward : Send reward (arm, reward, x)
- POST /tirages : Send tirages (generated random for moment)

# Exemple request :

## Get current theta values :
```bash
curl -X GET \
  http://127.0.0.1:8080/thetas \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/x-www-form-urlencoded' \
```

## Pick arm :
```bash
curl -X POST \
  http://127.0.0.1:8080/tirages \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/x-www-form-urlencoded' \
```

## Post reward :
```bash
curl -X POST \
  http://127.0.0.1:8080/reward \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/x-www-form-urlencoded' \
  -d 'arm=0&reward=100&x=%5B0.99109423889623149%2C%200.99403990262967967%2C%200.11750633515302655%5D'
```

## Add arm :
```bash
curl -X POST \
  http://127.0.0.1:8080/arms \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/x-www-form-urlencoded' \
  -d n_arms=5
```

# TODO :
- Remove feature (array -> dict)
