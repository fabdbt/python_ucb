# docker build -t python_ucb .
# sudo docker run -it --rm -p 443:443 -v /home/fabien/Workspace/python_ucb/storage:/storage -v /tmp/cert.pem:/cert.pem -v /tmp/cert.key:/cert.key -e LINUCB_AUTH_KEY=private_token python_ucb
# docker run -it --rm -p 8080:8080 -v /home/fabien/Workspace/python_ucb/storage:/storage -e LINUCB_AUTH_KEY=private_token python_ucb

FROM python:3.6-slim
MAINTAINER Fabien Dobat 'fabien.dobat@gmail.com'

RUN apt-get update
RUN apt-get install python3-tk -y
RUN pip3 install numpy scipy matplotlib

COPY ./src /src

EXPOSE 8080
CMD [ "python3", "./src/server.py" ]
