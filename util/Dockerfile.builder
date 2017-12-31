FROM python:3-slim

RUN apt-get update -qq
RUN apt-get install tree binutils jq curl -qqy
RUN pip3 install pyinstaller
