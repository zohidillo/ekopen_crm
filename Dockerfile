FROM python:3.11.1

WORKDIR /usr/src/app

ENV PYTHONDONTWRITENYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip install --upgrade pip

COPY requirements.txt /usr/src/app

RUN python -m pip install gunicorn
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /usr/src/app
EXPOSE 8000