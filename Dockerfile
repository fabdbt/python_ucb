# docker build -t python_ucb .
# docker run -it --rm -p 8080:8080 python_ucb

FROM python:3.6-slim
MAINTAINER Fabien Dobat 'fabien.dobat@gmail.com'

RUN apt-get update
RUN apt-get install python3-tk -y
RUN pip3 install numpy scipy matplotlib

COPY . /src

EXPOSE 8080
CMD [ "python3", "./src/server.py" ]
