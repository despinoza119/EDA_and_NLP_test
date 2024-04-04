# TBD
FROM python:3.11-slim

RUN pip install poetry

WORKDIR /usr/src/app

COPY ./ /usr/src/app

RUN poetry install

WORKDIR /usr/src/app/project

EXPOSE 8501

CMD [ "poetry", "run", "streamlit", "run", "app.py"]
