FROM python:3.12-slim

ENV PYTHONPATH "${PYTHONPATH}:/project"

WORKDIR /project

COPY pyproject.toml ./

RUN pip install .
