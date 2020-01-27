# docker build -t python_ucb .
# docker run -it --rm -p 8080:8080 -v /home/fabien/Workspace/python_ucb/storage:/storage -e LINUCB_AUTH_KEY=private_token python_ucb

FROM python:3.6-slim
LABEL maintainer="fabien.dobat@gmail.com"

RUN apt-get update
RUN apt-get install python3-tk -y

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./src /src

EXPOSE 8080
CMD [ "python3", "./src/server.py" ]
