# Description
A simple HTTP server that handle requests to feed a LinUCB machine learning algorithm

# Dependencies
- Python 3

# How to run it ?
```bash
python3 server.py
```

# Endpoints:
- GET /thetas : Get current thetas values
- POST /teams : Update teams

# Exemple request :
```bash
curl -X GET \
  http://127.0.0.1:8080/thetas \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/x-www-form-urlencoded' \
  -H 'postman-token: 63d26158-1f7c-5519-bc01-651e54dd9e0a' \
  -d 'dze=de&a=c&d=zedez'
```
