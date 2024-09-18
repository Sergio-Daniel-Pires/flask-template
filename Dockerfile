FROM python:3.12-slim

ENV PYTHONPATH "${PYTHONPATH}:/flask-template"

WORKDIR /project

COPY pyproject.toml ./

RUN pip install .
