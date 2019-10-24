FROM python:2.7.12
# maintainer
MAINTAINER zxy@cyberpeace.com
ENV PYTHONUNBUFFERED 1
COPY requirements.txt ./
RUN pip install -r requirements.txt -i https://pypi.doubanio.com/simple